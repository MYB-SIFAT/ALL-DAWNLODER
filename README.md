<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0a,50:1a1a1a,100:0a0a0a&height=200&section=header&text=ALL%20DAWNLODER&fontSize=60&fontColor=ffffff&fontAlignY=40&desc=Download%20Anything.%20From%20Anywhere.&descSize=18&descAlignY=62&descColor=888888" width="100%"/>

<br>

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-Powered-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live-22C55E?style=for-the-badge&logo=statuspage&logoColor=white)]()

<br>

> **Free · Open Source · Self-Hosted · No Login · No Ads**
>
> Paste any video URL — get your file in seconds.  
> Powered by `yt-dlp` · Supports **1000+ platforms** worldwide.

<br>

[🌐 Live Demo](#) &nbsp;·&nbsp; [📖 API Docs](#-api-reference) &nbsp;·&nbsp; [🐛 Report Bug](https://github.com/MYB-SIFAT/all-dawnloder/issues) &nbsp;·&nbsp; [⭐ Star this Repo](https://github.com/MYB-SIFAT/all-dawnloder)

</div>

---

## 📸 Screenshots

<div align="center">

| 🏠 Homepage | 🌐 Platforms | 🍪 Cookie Manager |
|:---:|:---:|:---:|
| Paste URL → Preview → Choose Quality | Browse all 1000+ supported sites | Setup per-platform cookies |

</div>

---

## ✨ Features

<table>
<tr>
<td valign="top" width="50%">

### 🎯 Core Features
- ✅ Auto-detect platform from any URL
- ✅ Video thumbnail & title preview before download
- ✅ 4 quality options (Best HD · 720p · 480p · MP3)
- ✅ Real-time download progress bar + speed
- ✅ Multi-method fallback engine (never fails)
- ✅ Concurrent fragment downloads (5x speed)
- ✅ Download history — last 10 downloads

</td>
<td valign="top" width="50%">

### 🔐 Cookie & Auth
- ✅ Per-platform cookie support
- ✅ Load cookies from **file** or **env var** (Base64)
- ✅ Smart cookie priority system
- ✅ Built-in cookie test tool
- ✅ Supports private, login-required & age-restricted content
- ✅ Temp cookie files auto-cleaned every hour

</td>
</tr>
<tr>
<td valign="top">

### 🎨 UI / UX
- ✅ Minimal black & white design
- ✅ Auto-analyze URL on paste
- ✅ Smooth animations & transitions
- ✅ Side navigation menu
- ✅ Toast notifications
- ✅ Fully mobile responsive

</td>
<td valign="top">

### ☁️ Deployment & Ops
- ✅ Docker image with FFmpeg built-in
- ✅ One-click Render.com deploy
- ✅ Railway deploy support
- ✅ Gunicorn production server
- ✅ Auto file cleanup after 24 hours
- ✅ REST API for external integrations

</td>
</tr>
</table>

---

## 🌐 Supported Platforms

<div align="center">

| Category | Count | Platforms |
|---|:---:|---|
| 🔥 **Most Popular** | 4 | YouTube · Instagram · TikTok · Facebook |
| 📱 **Social Media** | 10 | Twitter/X · Reddit · Pinterest · Snapchat · LinkedIn · Tumblr · VK · Weibo · MeWe · Mastodon |
| 🎬 **Video** | 16 | Vimeo · Dailymotion · Twitch · Bilibili · Rumble · Odysee · Kick · Streamable · Niconico + more |
| 🎵 **Music & Audio** | 10 | SoundCloud · Bandcamp · Mixcloud · Audiomack · Deezer · Tidal + more |
| 📰 **News & Media** | 12 | BBC · CNN · Al Jazeera · Reuters · Bloomberg · DW · Sky News + more |
| 🎭 **Entertainment** | 12 | Crunchyroll · Funimation · 9GAG · Hotstar · MX Player · ZEE5 + more |
| ⚽ **Sports** | 8 | ESPN · NBA · NFL · UEFA · Formula 1 · WWE · UFC + more |
| 📚 **Education** | 10 | Coursera · Udemy · Khan Academy · TED · edX · Skillshare + more |
| ➕ **And many more** | 1000+ | Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) |

</div>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Version |
|---|---|:---:|
| **Language** | Python | 3.11+ |
| **Web Framework** | Flask | 3.0.0 |
| **WSGI Server** | Gunicorn | 21.2.0 |
| **Download Engine** | yt-dlp | 2026.06.09 |
| **Media Processing** | FFmpeg | Latest |
| **Database** | SQLite | Built-in |
| **CORS** | flask-cors | 4.0.0 |
| **Frontend** | Vanilla JS + Lucide Icons | — |
| **Container** | Docker (python:3.12-slim) | — |

</div>

---

## 📁 Project Structure

```
all-dawnloder/
│
├── 📄 main.py                  ← Flask app — routes, download engine, DB logic
├── 📄 app.py                   ← Entry point (imports from main)
│
├── 📂 templates/               ← Jinja2 HTML pages
│   ├── base.html               ← Shared layout, navbar, footer
│   ├── index.html              ← Homepage (downloader UI)
│   ├── platforms.html          ← Supported platforms list
│   ├── history.html            ← Download history
│   ├── cookies.html            ← Cookie manager & setup guide
│   └── developer.html          ← API documentation page
│
├── 📂 static/
│   ├── css/style.css           ← All styles (2300+ lines)
│   └── js/app.js               ← Frontend logic (polling, history, UI)
│
├── 📂 Cookies/                 ← Drop cookie .txt files here
│   ├── youtube.txt
│   ├── facebook.txt
│   ├── instagram.txt
│   ├── tiktok.txt
│   └── twitter.txt
│
├── 📂 downloads/               ← Completed files (auto-deleted after 24h)
├── 📂 temp/                    ← Temp cookie files (auto-cleaned hourly)
├── 📄 downloads.db             ← SQLite: download history
│
├── 🐳 Dockerfile               ← Docker build (includes FFmpeg)
├── 📄 Procfile                 ← Gunicorn start command
├── 📄 render.yaml              ← Render.com config
├── 📄 railway.toml             ← Railway config
├── 📄 nixpacks.toml            ← Nixpacks build config
├── 📄 requirements.txt         ← Python dependencies
├── 📄 runtime.txt              ← Python version pin
├── 📄 run.sh                   ← Linux/macOS quick-start script
└── 📄 run.bat                  ← Windows quick-start script
```

---

## 🚀 Quick Start

### ▶️ Option 1 — Run Locally (Python)

```bash
# 1. Clone the repository
git clone https://github.com/MYB-SIFAT/all-dawnloder.git
cd all-dawnloder

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install FFmpeg (required for merging video+audio & MP3 extraction)
#    Ubuntu / Debian:
sudo apt install ffmpeg
#    macOS:
brew install ffmpeg
#    Windows: Download from https://ffmpeg.org/download.html

# 4. Start the server
python main.py
```

🌐 Open **[http://localhost:5000](http://localhost:5000)**

---

### 🐳 Option 2 — Docker (Recommended for Production)

```bash
# Build the image
docker build -t all-dawnloder .

# Run the container
docker run -p 5000:5000 all-dawnloder
```

**With persistent storage + cookies:**
```bash
docker run -p 5000:5000 \
  -v $(pwd)/downloads:/app/downloads \
  -v $(pwd)/Cookies:/app/Cookies \
  -e YOUTUBE_COOKIES="your_base64_cookie_here" \
  all-dawnloder
```

---

### 🪟 Option 3 — Windows Quick Start

```bat
run.bat
```
or
```bash
bash run.sh
```

---

## ☁️ Deploy to Cloud

### 🟣 Render.com *(Free Tier Available)*

| Step | Action |
|:---:|---|
| 1 | Fork this repository to your GitHub |
| 2 | Go to [render.com](https://render.com) → **New** → **Web Service** |
| 3 | Connect your forked repo |
| 4 | Render auto-reads `render.yaml` — just click **Deploy** |
| 5 | Set environment variables (cookies) in Render dashboard if needed |

> ✅ FFmpeg is automatically included in the Docker image.

---

### 🚂 Railway

| Step | Action |
|:---:|---|
| 1 | Fork this repository to your GitHub |
| 2 | Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub** |
| 3 | Select your forked repo |
| 4 | Railway auto-reads `railway.toml` + `nixpacks.toml` |
| 5 | Add environment variables → **Deploy** |

---

## 🍪 Cookie Setup *(Optional)*

Cookies unlock **age-restricted**, **private**, and **login-required** content.

### 📥 Step 1 — Export Cookies

Install the **[Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)** Chrome extension (Netscape format).

### 📂 Method 1 — Cookie Files (Local / VPS)

Drop your exported `.txt` files into the `Cookies/` folder:

```
Cookies/
├── youtube.txt       ← YouTube cookies
├── facebook.txt      ← Facebook cookies
├── instagram.txt     ← Instagram cookies
├── tiktok.txt        ← TikTok cookies
└── twitter.txt       ← Twitter/X cookies
```

### 🌍 Method 2 — Environment Variables (Hosting)

Base64-encode your cookie and set it as an env var in your hosting platform:

```bash
# Encode your cookie file (Linux/macOS)
base64 -w 0 youtube.txt

# Then set in your platform's environment variables:
YOUTUBE_COOKIES=eWVzY29va2llY29udGVudGhlcmU...
```

| Environment Variable | Platform |
|---|---|
| `YOUTUBE_COOKIES` | YouTube |
| `FACEBOOK_COOKIES` | Facebook |
| `INSTAGRAM_COOKIES` | Instagram |
| `TIKTOK_COOKIES` | TikTok |
| `TWITTER_COOKIES` | Twitter / X |
| `COOKIES` | Generic fallback (all platforms) |

### 🔢 Cookie Priority Order

```
PLATFORM_COOKIES (env)  →  COOKIES (env)  →  Cookies/<platform>.txt  →  Cookies/cookies.txt  →  cookies.txt
```

> 💡 Use the **Cookie Test** tool at `/cookies` to verify your cookies work before downloading.

---

## 🔌 API Reference

> **Base URL:** `http://your-domain.com`  
> All endpoints accept/return `application/json`

---

### `POST /api/analyze`

Fetch video metadata without downloading.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "title": "Rick Astley - Never Gonna Give You Up",
  "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
  "platform": "YouTube",
  "duration": "3:33"
}
```

---

### `POST /api/download`

Start a background download. Returns a download `id` immediately.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "format": "best"
}
```

| `format` | Description | Output |
|---|---|---|
| `best` | Highest quality video | MP4 (merged with FFmpeg) |
| `medium` | 720p | MP4 |
| `small` | 480p | MP4 |
| `audio` | Audio only, 192kbps | MP3 |

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### `GET /api/status/<id>`

Poll download progress in real-time.

**Response:**
```json
{
  "status": "downloading",
  "progress": "67.3",
  "speed": "2.50MiB/s",
  "title": "Rick Astley - Never Gonna Give You Up",
  "thumbnail": "https://..."
}
```

| `status` | Meaning |
|---|---|
| `starting` | Initializing download |
| `downloading` | Actively downloading |
| `processing_files` | Merging / converting with FFmpeg |
| `completed` | File ready — use `/file/<id>` |
| `error` | Download failed |

---

### `GET /file/<id>`

Serve the completed file as a download.

```
GET /file/550e8400-e29b-41d4-a716-446655440000
→ Content-Disposition: attachment; filename="Rick_Astley_Never_Gonna_Give_You_Up.mp4"
```

---

### `GET /api/history`

Returns the last 10 completed downloads.

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Rick Astley - Never Gonna Give You Up",
    "platform": "YouTube",
    "thumbnail": "https://...",
    "date": "2026-06-20T12:00:00",
    "filename": "Rick_Astley_Never_Gonna_Give_You_Up.mp4"
  }
]
```

---

### `GET /api/cookies/status`

Check which platforms have cookies configured.

**Response:**
```json
{
  "youtube":   { "configured": true,  "method": "file", "file": "Cookies/youtube.txt" },
  "facebook":  { "configured": true,  "method": "env",  "var": "FACEBOOK_COOKIES" },
  "instagram": { "configured": false },
  "tiktok":    { "configured": false },
  "twitter":   { "configured": false }
}
```

---

### `POST /api/test-cookie/<platform>`

Test if a cookie is working for a specific platform.

```
POST /api/test-cookie/youtube
```

**Response (success):**
```json
{
  "success": true,
  "message": "Cookie works! ✓ Found: \"Never Gonna Give You Up\""
}
```

**Response (failure):**
```json
{
  "success": false,
  "message": "Cookie expired or invalid — re-export fresh cookies from your browser."
}
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|:---:|---|
| `PORT` | `5000` | Server listening port |
| `YOUTUBE_COOKIES` | — | Base64-encoded YouTube cookie |
| `FACEBOOK_COOKIES` | — | Base64-encoded Facebook cookie |
| `INSTAGRAM_COOKIES` | — | Base64-encoded Instagram cookie |
| `TIKTOK_COOKIES` | — | Base64-encoded TikTok cookie |
| `TWITTER_COOKIES` | — | Base64-encoded Twitter/X cookie |
| `COOKIES` | — | Generic fallback cookie (all platforms) |

---

## 🔄 Download Engine — How It Works

```
  ┌─────────────────────────────────────────────────┐
  │           User pastes URL                       │
  └──────────────────────┬──────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Detect Platform    │
              │  (YouTube/IG/etc.)  │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │  Load Cookie File   │ ← env var or file
              │  (if available)     │
              └──────────┬──────────┘
                         │
         ┌───────────────▼────────────────┐
         │    Method 1: Best Quality      │ MP4 + M4A → FFmpeg merge
         └───────────────┬────────────────┘
                    ✗ fails
         ┌───────────────▼────────────────┐
         │    Method 2: Fallback Format   │ 720p or platform-specific
         └───────────────┬────────────────┘
                    ✗ fails
         ┌───────────────▼────────────────┐
         │    Method 3: Basic Download    │ any available format
         └───────────────┬────────────────┘
                    ✗ fails (YouTube only)
         ┌───────────────▼────────────────┐
         │    Method 4: Audio Fallback    │ MP3 @ 192kbps
         └───────────────┬────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Sanitize Filename  │
              │  Save to DB         │
              │  Serve Download     │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │  Auto-delete        │ after 24 hours
              │  (cleanup loop)     │
              └─────────────────────┘
```

---

## 📦 Dependencies

```txt
Flask==3.0.0           # Web framework
flask-cors==4.0.0      # Cross-Origin Resource Sharing
yt-dlp==2026.06.09     # Video extraction & download
Werkzeug==3.0.1        # WSGI utilities
gunicorn==21.2.0       # Production WSGI server
ffmpeg (system)        # Audio/video processing & merging
```

---

## 👨‍💻 Author

<div align="center">

<img src="https://github.com/MYB-SIFAT.png" width="110" style="border-radius: 50%; border: 3px solid #222;"/>

### SIFAT

**Open Source Developer & Content Creator**  
🇧🇩 Bangladesh

<br>

[![GitHub](https://img.shields.io/badge/GitHub-MYB--SIFAT-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MYB-SIFAT)
[![YouTube](https://img.shields.io/badge/YouTube-@mybsifat-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/@mybsifat)
[![Telegram](https://img.shields.io/badge/Telegram-MaybeSifu-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/MaybeSifu)

<br>

*"Building free tools for everyone."*

</div>

---

## 📄 License

```
MIT License

Copyright (c) 2026 SIFAT (MYB-SIFAT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

Full license → [LICENSE](LICENSE)

---

## ⭐ Show Your Support

If **ALL DAWNLODER** helped you, please give it a ⭐ on GitHub!  
It helps others discover the project and motivates me to keep building.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0a,100:1a1a1a&height=120&section=footer&text=ALL%20DAWNLODER%20v1.0.0&fontSize=20&fontColor=555555&fontAlignY=65" width="100%"/>

**Made with ❤️ by [SIFAT](https://github.com/MYB-SIFAT) · Bangladesh · 2026**

</div>
