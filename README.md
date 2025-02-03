# 🎵 YouTube Playlist Manager

Easily create YouTube playlists from an Excel file 📂 or export existing YouTube playlists to an Excel file 📥 using this simple tool built with Streamlit and the YouTube API! 🚀

---

## ✨ Features
- ✅ **Create a YouTube playlist** from a list of video URLs in an Excel file (.xlsx)
- ✅ **Export a YouTube playlist** to an Excel file for easy sharing or backup
- ✅ **Simple UI** built with Streamlit 🎨
- ✅ **OAuth 2.0 Authentication** for secure YouTube access 🔑

---

## 📦 Installation

First, clone this repository and navigate to the project directory:
```sh
 git clone https://github.com/yourusername/youtube-playlist-manager.git
 cd youtube-playlist-manager
```

Create a virtual environment (optional but recommended):
```sh
 python -m venv venv
 source venv/bin/activate  # On macOS/Linux
 venv\Scripts\activate    # On Windows
```

Install the required dependencies:
```sh
 pip install -r requirements.txt
```

---

## 🔑 Setup Google API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project and enable the **YouTube Data API v3**
3. Set up **OAuth 2.0 Client ID** and download the `client_secret.json` file
4. Place `client_secret.json` in the project folder

---

## 🚀 Usage

### 📝 1. Create a Playlist from Excel
1. Run the app using:
   ```sh
   streamlit run app.py
   ```
2. Navigate to the **Create Playlist** tab 📂
3. Enter a playlist name and description
4. Upload an Excel file (`.xlsx`) with a **column named `URL`** containing YouTube video links
5. Click **Create Playlist** and watch your playlist appear on YouTube! 🎶

✅ **Example Excel File Format:**
| URL                                      |
|-----------------------------------------|
| https://www.youtube.com/watch?v=abc123 |
| https://www.youtube.com/watch?v=xyz789 |


### 📥 2. Export a YouTube Playlist to Excel
1. Navigate to the **Export Playlist** tab
2. Paste the YouTube playlist URL (e.g., `https://www.youtube.com/playlist?list=PL1234567890`)
3. Click **Export Playlist**
4. Download the generated Excel file 📄

✅ **Example Exported File Format:**
| Title              | Video URL                                |
|-------------------|-----------------------------------------|
| My Favorite Song | https://www.youtube.com/watch?v=abc123 |
| Another Hit      | https://www.youtube.com/watch?v=xyz789 |

---

## 🛠️ Troubleshooting

- **Getting `invalid_grant: Bad Request`?**
  - Delete `token.json` and re-authenticate
- **Blank playlist created?**
  - Ensure URLs in the Excel file are valid YouTube links
- **App crashes when uploading an Excel file?**
  - Verify the Excel file contains a column named `URL`

---

## 🏗️ Future Improvements
- 🔄 **Edit existing playlists**
- 🎨 **Better UI & progress tracking**
- 📊 **Analytics on exported playlists**

---

## 📜 License
This project is open-source under the **MIT License**. Feel free to modify and improve! 🎉

---

## 💬 Support & Feedback
If you find any bugs 🐞 or have feature requests, feel free to open an issue or contribute! 😊

