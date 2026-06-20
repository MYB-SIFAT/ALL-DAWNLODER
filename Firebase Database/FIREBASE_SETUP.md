<div align="center">

<img src="https://img.shields.io/badge/StreamVault-Firebase%20Firestore%20Setup-FF6B35?style=for-the-badge&logo=firebase&logoColor=white" />

<br/>
<br/>

<img src="https://img.shields.io/badge/Database-Firestore-FFCA28?style=flat-square&logo=firebase&logoColor=black" />
<img src="https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render&logoColor=black" />
<img src="https://img.shields.io/badge/Backend-Python%20%2F%20Flask-3776AB?style=flat-square&logo=python&logoColor=white" />

</div>

---

StreamVault uses **Firebase Firestore** so that all download history persists across restarts when deployed to Render. If no credentials are found, the app automatically falls back to in-memory storage.

---

## <img src="https://img.shields.io/badge/-Setup%20Steps-161b22?style=flat-square&logo=gitbook&logoColor=white" /> Setup Steps

### <img src="https://img.shields.io/badge/1-Create%20Firebase%20Project-FF6B35?style=flat-square" />

1. Go to: https://console.firebase.google.com/
2. Click **"Add project"**
3. Enter a project name (e.g. `streamvault`)
4. Disable Google Analytics (optional)
5. Click **"Create project"**

---

### <img src="https://img.shields.io/badge/2-Enable%20Firestore%20Database-FF6B35?style=flat-square" />

1. Open **"Firestore Database"** from the left sidebar
2. Click **"Create database"**
3. Select **Production mode**
4. Choose a location (e.g. `asia-south1`)
5. Click **"Enable"**

---

### <img src="https://img.shields.io/badge/3-Download%20Service%20Account%20Key-FF6B35?style=flat-square" />

1. Go to **Project Settings** (gear icon in sidebar)
2. Click the **"Service accounts"** tab
3. Scroll down and click **"Generate new private key"**
4. Confirm — a JSON file will be downloaded
5. Rename the file to `firebase-credentials.json`

---

### <img src="https://img.shields.io/badge/4-Configure%20Credentials-FF6B35?style=flat-square" />

**Local Development** — place the file at the project root:

```
streamvault_ultimate/
├── firebase-credentials.json   ← place here
├── main.py
├── requirements.txt
└── ...
```

**Render Deployment** — go to your service → **Environment** tab → add:

```
Key:   FIREBASE_CREDENTIALS
Value: { "type": "service_account", "project_id": "your-project-id", ... }
```

> [!IMPORTANT]
> Paste the **entire JSON content** — including all curly braces — as the variable value.

---

## <img src="https://img.shields.io/badge/-Running%20the%20App-161b22?style=flat-square&logo=gnubash&logoColor=white" /> Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Start the app
python main.py
```

> [!NOTE]
> **With Firestore:** `Firestore initialized with credentials file`
>
> **Without credentials:** `Firebase credentials not found. Using in-memory storage.`

---

## <img src="https://img.shields.io/badge/-Database%20Structure-161b22?style=flat-square&logo=amazondynamodb&logoColor=white" /> Database Structure

```
Collection: history
└── Document: {download_id}
    ├── id         "abc-123-xyz"
    ├── url        "https://youtube.com/watch?v=..."
    ├── title      "Video Title"
    ├── platform   "YouTube"
    ├── filename   "video.mp4"
    ├── thumbnail  "https://..."
    ├── timestamp  2024-02-15T10:30:00
    └── expiry     2024-02-16T10:30:00  (24h later)
```

---

## <img src="https://img.shields.io/badge/-Features-161b22?style=flat-square&logo=sparkles&logoColor=white" /> Features

| | Feature | Description |
|---|---|---|
| <img src="https://img.shields.io/badge/✓-green?style=flat-square" /> | **Automatic Fallback** | Uses in-memory storage when Firestore credentials are not configured |
| <img src="https://img.shields.io/badge/✓-green?style=flat-square" /> | **Render Compatible** | Deploy via environment variables — no file uploads needed |
| <img src="https://img.shields.io/badge/✓-green?style=flat-square" /> | **Auto Cleanup** | Runs every hour to delete records and files older than 24 hours |
| <img src="https://img.shields.io/badge/✓-green?style=flat-square" /> | **History Tracking** | Every download is saved with full metadata and expiry info |
| <img src="https://img.shields.io/badge/✓-green?style=flat-square" /> | **Persistent Storage** | Cloud-backed — no data loss on server restarts or redeployments |

---

## <img src="https://img.shields.io/badge/-Deploy%20to%20Render-46E3B7?style=flat-square&logo=render&logoColor=black" /> Deploying to Render

**1.** Add environment variable in Render dashboard:
```
FIREBASE_CREDENTIALS = {paste entire JSON here}
```

**2.** Build Command:
```bash
pip install -r requirements.txt
```

**3.** Start Command:
```bash
gunicorn main:app
```

**4.** Trigger a deploy — the app will connect to Firestore immediately.

---

## <img src="https://img.shields.io/badge/-Troubleshooting-161b22?style=flat-square&logo=searchengineland&logoColor=white" /> Troubleshooting

> [!CAUTION]
> **`Firebase initialization failed`**
> - Verify that `firebase-credentials.json` exists in the project root
> - Check that the JSON is valid and not truncated
> - Confirm that Firestore is enabled in your Firebase console

> [!WARNING]
> **`Using in-memory storage`**
> - Safe for local testing — no action needed
> - For production, set `FIREBASE_CREDENTIALS` on Render
> - Data in memory will **not** survive a server restart

---

## <img src="https://img.shields.io/badge/-Support-161b22?style=flat-square&logo=googlechat&logoColor=white" /> Support

<div align="center">

[![Email](https://img.shields.io/badge/Email-siamxus69%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:siamxus69@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-@SiamBhau-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/SiamBhau69)
[![Facebook](https://img.shields.io/badge/Facebook-SiamBhau-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://facebook.com/SiamBhau2.0)

</div>

---

<div align="center">
<sub>Made with ❤️ by <a href="https://github.com/SiamBhau">SiamBhau</a></sub>
</div>
