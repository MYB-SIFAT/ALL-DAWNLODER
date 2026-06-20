<div align="center">

<img src="https://img.shields.io/badge/Stream-Vault-000000?style=for-the-badge&logo=youtube&logoColor=white" height="40"/>

### Premium Media Downloader — Beautiful UI · Multi-Platform · Real-time Progress

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=flat-square&logo=firebase&logoColor=black)
![yt-dlp](https://img.shields.io/badge/yt--dlp-FF0000?style=flat-square&logo=youtube&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render&logoColor=black)

</div>

---

## Features

| | Feature | Details |
|---|---|---|
| ![](https://img.shields.io/badge/-UI-black?style=flat-square) | **Gorgeous Design** | Professional white & black theme |
| ![](https://img.shields.io/badge/-DL-black?style=flat-square) | **Smart Download** | Analyze → Choose Quality → Download |
| ![](https://img.shields.io/badge/-Live-black?style=flat-square) | **Real-time Progress** | Live progress bar with percentage |
| ![](https://img.shields.io/badge/-Multi-black?style=flat-square) | **Multiple Platforms** | YouTube, Facebook, Instagram, TikTok, Twitter & more |
| ![](https://img.shields.io/badge/-4K-black?style=flat-square) | **Quality Options** | Best, HD 720p, Mobile, Audio MP3 |
| ![](https://img.shields.io/badge/-24h-black?style=flat-square) | **Auto Storage** | Files stored for 24 hours then auto-deleted |
| ![](https://img.shields.io/badge/-DB-black?style=flat-square) | **History** | All downloads tracked via Firestore |

---

## Quick Start

**Linux / Mac**
```bash
chmod +x run.sh && ./run.sh
```

**Windows**
```bash
run.bat
```

Then open **http://localhost:5000**

---

## How to Use

```
1. Paste URL      →   Drop any video link into the input
2. Click Analyze  →   Platform is detected automatically
3. Choose Quality →   Best / HD 720p / Mobile / MP3
4. Download       →   Watch the real-time progress bar
5. Get File       →   Grab your file from History
```

---

## Supported Platforms

<details>
<summary><b>Video Platforms (click to expand)</b></summary>

| Platform | URLs |
|---|---|
| ![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=flat-square&logo=youtube&logoColor=white) | `youtube.com`, `youtu.be` |
| ![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=flat-square&logo=facebook&logoColor=white) | `facebook.com`, `fb.watch`, `m.facebook.com` |
| ![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white) | `instagram.com`, `instagr.am`, Reels, Stories |
| ![TikTok](https://img.shields.io/badge/TikTok-000000?style=flat-square&logo=tiktok&logoColor=white) | `tiktok.com`, `vm.tiktok.com` |
| ![Twitter](https://img.shields.io/badge/Twitter%2FX-000000?style=flat-square&logo=x&logoColor=white) | `twitter.com`, `x.com`, `t.co` |
| ![Vimeo](https://img.shields.io/badge/Vimeo-1AB7EA?style=flat-square&logo=vimeo&logoColor=white) | `vimeo.com` |
| ![Dailymotion](https://img.shields.io/badge/Dailymotion-0066DC?style=flat-square&logo=dailymotion&logoColor=white) | `dailymotion.com`, `dai.ly` |
| ![Reddit](https://img.shields.io/badge/Reddit-FF4500?style=flat-square&logo=reddit&logoColor=white) | `reddit.com`, `redd.it` |
| ![Twitch](https://img.shields.io/badge/Twitch-9146FF?style=flat-square&logo=twitch&logoColor=white) | `twitch.tv` |

</details>

<details>
<summary><b>Audio Platforms (click to expand)</b></summary>

| Platform | URLs |
|---|---|
| ![SoundCloud](https://img.shields.io/badge/SoundCloud-FF3300?style=flat-square&logo=soundcloud&logoColor=white) | `soundcloud.com` |
| ![Bandcamp](https://img.shields.io/badge/Bandcamp-1DA0C3?style=flat-square&logo=bandcamp&logoColor=white) | `bandcamp.com` |

</details>

> Powered by **yt-dlp** — supports 1000+ sites out of the box.

### Enhanced Facebook Support

- All formats: `fb.watch`, mobile links, desktop links
- Facebook Reels & Facebook Watch
- Private videos (with proper authentication)
- Multiple fallback methods for reliability

---

## Firebase Setup

> Need persistent storage for Render deployment? See the full guide:

[![Firebase Setup Guide](https://img.shields.io/badge/Read-Firebase%20Setup%20Guide-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](./FIREBASE_SETUP.md)

---

## Project Structure

```
streamvault_ultimate/
├── main.py                          # Flask app + Firestore logic
├── requirements.txt                 # Python dependencies
├── firebase-credentials.example.json
├── run.sh                           # Linux/Mac launcher
├── run.bat                          # Windows launcher
├── templates/
│   └── index.html                   # Main UI
├── static/
│   ├── css/style.css
│   └── js/app.js
├── downloads/                       # Served download files
└── temp/                            # Temp processing dir
```

---

## Contact

<div align="center">

[![Facebook](https://img.shields.io/badge/Facebook-SiamBhau69-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://facebook.com/SiamBhau2.0)
[![Telegram](https://img.shields.io/badge/Telegram-@SiamBhau69-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/SiamBhau69)
[![Email](https://img.shields.io/badge/Email-siamxus69@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:siamxus69@gmail.com)

</div>

---

<div align="center">
<sub>Made with ❤️ by <a href="https://github.com/SiamBhau">SiamBhau</a></sub>
</div>
