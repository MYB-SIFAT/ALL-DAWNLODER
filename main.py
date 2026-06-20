from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import threading
import time
import sqlite3
import base64
import tempfile
import re
import hashlib
import concurrent.futures
from datetime import datetime, timedelta
from yt_dlp import YoutubeDL
import logging

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = 'downloads'
TEMP_DIR = 'temp'
COOKIES_DIR = 'Cookies'
DB_PATH = 'downloads.db'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(COOKIES_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

download_state = {}

PLATFORM_COOKIE_MAP = {
    'youtube':   ('YOUTUBE_COOKIES',   ['youtube.txt']),
    'facebook':  ('FACEBOOK_COOKIES',  ['facebook.txt']),
    'instagram': ('INSTAGRAM_COOKIES', ['instagram.txt']),
    'tiktok':    ('TIKTOK_COOKIES',    ['tiktok.txt']),
    'twitter':   ('TWITTER_COOKIES',   ['twitter.txt']),
}

def _write_temp_cookie(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', delete=False,
        dir=TEMP_DIR, prefix='cookie_'
    )
    tmp.write(content)
    tmp.close()
    return tmp.name


def get_cookie_file(platform: str):
    platform_key = platform.lower()
    env_var, filenames = PLATFORM_COOKIE_MAP.get(
        platform_key, ('COOKIES', [])
    )

    for var in [env_var, 'COOKIES']:
        raw = os.environ.get(var, '').strip()
        if not raw:
            continue
        if '\t' in raw or raw.startswith('#'):
            return _write_temp_cookie(raw)
        try:
            decoded = base64.b64decode(raw).decode('utf-8')
            return _write_temp_cookie(decoded)
        except Exception:
            return _write_temp_cookie(raw)

    for fname in filenames:
        path = os.path.join(COOKIES_DIR, fname)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return path

    generic = os.path.join(COOKIES_DIR, 'cookies.txt')
    if os.path.exists(generic) and os.path.getsize(generic) > 0:
        return generic

    if os.path.exists('cookies.txt') and os.path.getsize('cookies.txt') > 0:
        return 'cookies.txt'

    return None


def cookies_status() -> dict:
    result = {}
    for platform_key, (env_var, filenames) in PLATFORM_COOKIE_MAP.items():
        for var in [env_var, 'COOKIES']:
            if os.environ.get(var, '').strip():
                result[platform_key] = {'configured': True, 'method': 'env', 'var': var}
                break
        else:
            found_file = None
            for fname in filenames:
                path = os.path.join(COOKIES_DIR, fname)
                if os.path.exists(path) and os.path.getsize(path) > 0:
                    found_file = fname
                    break
            if not found_file:
                for generic in [os.path.join(COOKIES_DIR, 'cookies.txt'), 'cookies.txt']:
                    if os.path.exists(generic) and os.path.getsize(generic) > 0:
                        found_file = generic
                        break
            if found_file:
                result[platform_key] = {'configured': True, 'method': 'file', 'file': found_file}
            else:
                result[platform_key] = {'configured': False}
    return result


class MyLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): logger.error(msg)


def progress_hook(d):
    download_id = d.get('info_dict', {}).get('download_id')
    if download_id and download_id in download_state:
        if d['status'] == 'downloading':
            download_state[download_id]['progress'] = d.get('_percent_str', '0%').replace('%', '').strip()
            download_state[download_id]['speed'] = d.get('_speed_str', 'N/A')
            download_state[download_id]['status'] = 'downloading'
        elif d['status'] == 'finished':
            download_state[download_id]['status'] = 'processing_files'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id TEXT PRIMARY KEY, url TEXT, title TEXT, platform TEXT, 
                  filename TEXT, thumbnail TEXT, timestamp DATETIME, expiry DATETIME)''')
    conn.commit()
    conn.close()


init_db()


def get_platform(url):
    url = url.lower()
    if 'youtube.com' in url or 'youtu.be' in url: return 'youtube'
    if 'instagram.com' in url: return 'instagram'
    if 'tiktok.com' in url: return 'tiktok'
    if 'twitter.com' in url or 'x.com' in url: return 'twitter'
    if 'facebook.com' in url or 'fb.com' in url: return 'facebook'
    return 'other'


def platform_display(platform_key):
    return {
        'youtube': 'YouTube', 'instagram': 'Instagram', 'tiktok': 'TikTok',
        'twitter': 'Twitter', 'facebook': 'Facebook', 'other': 'Social Media'
    }.get(platform_key, 'Social Media')


@app.route('/')
def index():
    return render_template('index.html', active_page='home')


@app.route('/platforms')
def platforms():
    return render_template('platforms.html', active_page='platforms')


@app.route('/history')
def history_page():
    return render_template('history.html', active_page='history')


@app.route('/developer')
def developer_page():
    return render_template('developer.html', active_page='developer')


@app.route('/cookies')
def cookies_page():
    status = cookies_status()
    return render_template('cookies.html', active_page='cookies', cookies_status=status)


@app.route('/api/cookies/status')
def api_cookies_status():
    return jsonify(cookies_status())


PLATFORM_TEST_URLS = {
    'youtube':   'https://www.youtube.com/watch?v=BaW_jenozKc',
    'facebook':  'https://www.facebook.com/FacebookforDevelopers/videos/10152454700553553/',
    'instagram': 'https://www.instagram.com/p/Cz5JqO-Ng8l/',
    'tiktok':    'https://www.tiktok.com/@tiktok/video/6584647400055377158',
    'twitter':   'https://x.com/Twitter/status/1445078208190291973',
}

@app.route('/api/test-cookie/<platform>', methods=['POST'])
def test_cookie(platform):
    platform = platform.lower()
    cookie_file = get_cookie_file(platform)

    if not cookie_file:
        return jsonify({'success': False, 'message': f'No cookie configured for {platform.capitalize()}.'})

    test_url = PLATFORM_TEST_URLS.get(platform)
    if not test_url:
        return jsonify({'success': False, 'message': f'No test URL available for {platform}.'})

    opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'socket_timeout': 15,
        'cookiefile': cookie_file,
    }

    def _extract():
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            return info.get('title', 'Video found')

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_extract)
            title = future.result(timeout=25)
        return jsonify({'success': True, 'message': f'Cookie works! ✓ Found: "{title[:60]}"'})
    except concurrent.futures.TimeoutError:
        return jsonify({'success': False, 'message': 'Test timed out (25s). Cookie may be invalid or network is slow.'})
    except Exception as e:
        err = str(e)
        if any(k in err.lower() for k in ['sign in', 'login', 'cookie', 'authentication', 'private']):
            return jsonify({'success': False, 'message': 'Cookie expired or invalid — re-export fresh cookies from your browser.'})
        return jsonify({'success': False, 'message': f'Test failed: {err[:200]}'})
    finally:
        if cookie_file and cookie_file.startswith(TEMP_DIR) and os.path.exists(cookie_file):
            try:
                os.unlink(cookie_file)
            except Exception:
                pass


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json(silent=True) or {}
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    platform = get_platform(url)
    cookie_file = get_cookie_file(platform)

    opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        'socket_timeout': 15,
    }
    if cookie_file:
        opts['cookiefile'] = cookie_file
        logger.info(f"Using cookie file for analyze: {cookie_file}")

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail'),
                'platform': platform_display(platform),
                'duration': info.get('duration_string')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        if cookie_file and cookie_file.startswith(TEMP_DIR) and os.path.exists(cookie_file):
            try:
                os.remove(cookie_file)
            except Exception:
                pass


@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json(silent=True) or {}
    url = data.get('url', '').strip()
    format_type = data.get('format', 'best')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    download_id = str(uuid.uuid4())
    download_state[download_id] = {
        'status': 'starting',
        'progress': '0',
        'title': 'Initializing...',
        'thumbnail': None
    }

    thread = threading.Thread(target=run_download, args=(download_id, url, format_type))
    thread.daemon = True
    thread.start()

    return jsonify({'id': download_id})


def run_download(download_id, url, format_type):
    cookie_file = None
    try:
        platform = get_platform(url)
        cookie_file = get_cookie_file(platform)

        if cookie_file:
            logger.info(f"[{download_id}] Using cookie file: {cookie_file}")

        info_opts = {'quiet': True, 'no_warnings': True}
        if cookie_file:
            info_opts['cookiefile'] = cookie_file
        with YoutubeDL(info_opts) as ydl:
            info_pre = ydl.extract_info(url, download=False)
            download_state[download_id]['title'] = info_pre.get('title', 'Video')
            download_state[download_id]['thumbnail'] = info_pre.get('thumbnail')

        opts = {
            'quiet': True,
            'no_warnings': False,
            'ignoreerrors': False,
            'logger': MyLogger(),
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(DOWNLOAD_DIR, f"{download_id}_%(title).100s.%(ext)s"),
            'restrictfilenames': True,
            'windowsfilenames': True,
            'concurrent_fragment_downloads': 5,
            'retries': 15,
            'fragment_retries': 15,
            'skip_unavailable_fragments': False,
            'socket_timeout': 20,
            'http_chunk_size': 10485760,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
        }

        if cookie_file:
            opts['cookiefile'] = cookie_file

        if platform == 'youtube':
            opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['configs', 'webpage'],
                }
            }

        if format_type == 'audio':
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif format_type == 'medium':
            opts['format'] = 'best[height<=720][ext=mp4]/best[height<=720]/best'
        elif format_type == 'small':
            opts['format'] = 'best[height<=480][ext=mp4]/best[height<=480]/worst'
        else:
            opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

        downloaded = False
        filename = None

        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                info['download_id'] = download_id
                filename = ydl.prepare_filename(info)
                if format_type == 'audio':
                    filename = os.path.splitext(filename)[0] + '.mp3'
                downloaded = True
        except Exception as e1:
            logger.warning(f"Method 1 failed: {str(e1)[:100]}")

            if platform == 'youtube' and format_type != 'audio':
                try:
                    alt_opts = opts.copy()
                    alt_opts['format'] = 'best[height<=720]' if format_type == 'best' else 'best[height<=480]'
                    with YoutubeDL(alt_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        info['download_id'] = download_id
                        filename = ydl.prepare_filename(info)
                        downloaded = True
                except Exception as e2:
                    logger.warning(f"Method 2 failed: {str(e2)[:100]}")

                    try:
                        audio_opts = opts.copy()
                        audio_opts['format'] = 'bestaudio'
                        audio_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]
                        with YoutubeDL(audio_opts) as ydl:
                            info = ydl.extract_info(url, download=True)
                            info['download_id'] = download_id
                            filename = ydl.prepare_filename(info)
                            filename = os.path.splitext(filename)[0] + '.mp3'
                            downloaded = True
                    except Exception as e3:
                        raise Exception(f"All download methods failed: {str(e3)}")
            else:
                raise e1

        if not downloaded or not filename:
            raise Exception("Download failed")

        if not os.path.exists(filename):
            base_name = os.path.splitext(filename)[0]
            for ext in ['.mp4', '.mkv', '.webm', '.mp3', '.m4a', '.m4v']:
                test_path = base_name + ext
                if os.path.exists(test_path):
                    filename = test_path
                    break

        if not os.path.exists(filename):
            raise Exception("Downloaded file not found")

        original_filename = os.path.basename(filename)
        sanitized = re.sub(r'[<>:"/\\|?*]', '', original_filename)
        sanitized = re.sub(r'[^\w\s.-]', '', sanitized)

        MAX_LENGTH = 100
        if len(sanitized) > MAX_LENGTH:
            name, ext = os.path.splitext(sanitized)
            name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
            sanitized = name[:MAX_LENGTH - len(ext) - 9] + '_' + name_hash + ext

        if original_filename != sanitized:
            new_path = os.path.join(os.path.dirname(filename), sanitized)
            os.rename(filename, new_path)
            filename = new_path

        final_filename = os.path.basename(filename)
        now_dt = datetime.now()
        expiry = now_dt + timedelta(hours=24)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO history VALUES (?,?,?,?,?,?,?,?)",
                  (download_id, url, info.get('title'), platform_display(platform),
                   final_filename, info.get('thumbnail'),
                   now_dt.isoformat(), expiry.isoformat()))
        conn.commit()
        conn.close()

        download_state[download_id]['status'] = 'completed'
        download_state[download_id]['filename'] = final_filename
        download_state[download_id]['progress'] = '100'
        download_state[download_id]['_done_at'] = time.time()

    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        download_state[download_id]['status'] = 'error'
        download_state[download_id]['error'] = str(e)
        download_state[download_id]['_done_at'] = time.time()
    finally:
        if cookie_file and cookie_file.startswith(TEMP_DIR) and os.path.exists(cookie_file):
            try:
                os.remove(cookie_file)
            except Exception:
                pass


@app.route('/api/status/<download_id>')
def status(download_id):
    state = download_state.get(download_id)
    if not state:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT title, filename, thumbnail FROM history WHERE id=?", (download_id,))
        res = c.fetchone()
        conn.close()
        if res:
            return jsonify({'status': 'completed', 'title': res[0], 'filename': res[1], 'thumbnail': res[2]})
        return jsonify({'status': 'not_found'})
    return jsonify(state)


@app.route('/api/history')
def history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, platform, thumbnail, timestamp, filename FROM history ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return jsonify([{
        'id': r[0], 'title': r[1], 'platform': r[2],
        'thumbnail': r[3], 'date': r[4], 'filename': r[5]
    } for r in rows])


@app.route('/file/<download_id>')
def get_file(download_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT filename FROM history WHERE id=?", (download_id,))
    res = c.fetchone()
    conn.close()
    if res:
        return send_from_directory(DOWNLOAD_DIR, res[0], as_attachment=True)
    return "File not found", 404


def cleanup_loop():
    while True:
        try:
            now = datetime.now()
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, filename FROM history WHERE expiry < ?", (now.isoformat(),))
            to_delete = c.fetchall()
            for fid, fname in to_delete:
                path = os.path.join(DOWNLOAD_DIR, fname)
                if os.path.exists(path):
                    os.remove(path)
                c.execute("DELETE FROM history WHERE id=?", (fid,))
            conn.commit()
            conn.close()

            now_ts = time.time()

            stale_ids = [
                k for k, v in list(download_state.items())
                if v.get('status') in ('completed', 'error')
                and now_ts - v.get('_done_at', now_ts) > 7200
            ]
            for sid in stale_ids:
                download_state.pop(sid, None)

            for fname in os.listdir(TEMP_DIR):
                if fname.startswith('cookie_') and fname.endswith('.txt'):
                    fpath = os.path.join(TEMP_DIR, fname)
                    try:
                        if now_ts - os.path.getmtime(fpath) > 3600:
                            os.remove(fpath)
                    except Exception:
                        pass
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
        time.sleep(3600)


threading.Thread(target=cleanup_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
