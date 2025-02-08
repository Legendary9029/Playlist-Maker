# YouTube Playlist Manager

## 📌 Overview
YouTube Playlist Manager is a **Streamlit-based web application** that allows users to **merge, create, and export YouTube playlists** efficiently. The application utilizes the **YouTube Data API** to automate playlist management tasks, enabling users to merge multiple public playlists, create new playlists from an Excel file, and export existing playlists to Excel.

## 🚀 Features
### 🔀 Merge Playlists
- Automatically merges videos from multiple **public YouTube playlists** into a **new playlist**.
- Requires no ownership of the original playlists.
- Progress tracking with a real-time **progress bar**.

### 📂 Create Playlist from Excel
- Users can upload an Excel file (`.xlsx`) containing video links.
- The app creates a new YouTube playlist with the provided videos.

### 📥 Export Playlist to Excel
- Exports the **video details** (title, video ID, etc.) from a YouTube playlist into an Excel file.
- Users can download the file directly.

## 🛠️ Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/youtube-playlist-manager.git
cd youtube-playlist-manager
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up YouTube API Credentials
- Create a **Google Cloud Project** and enable the **YouTube Data API v3**.
- Generate **OAuth 2.0 Client ID** credentials.
- Save your credentials as `client_secrets.json` in the project directory.

### 4️⃣ Run the Application
```sh
streamlit run app.py
```

## 🔧 Usage Guide
1. **Authenticate** using your Google account when prompted.
2. Navigate between tabs to **Merge Playlists, Create Playlists, or Export Playlists**.
3. Provide necessary inputs (playlist URLs, Excel files, etc.) and click the action buttons.
4. Download results if applicable.

## 🏗️ Technologies Used
- **Python** (Backend)
- **Streamlit** (Web UI)
- **YouTube Data API v3**
- **Pandas** (Excel Processing)
- **OAuth 2.0 Authentication**

## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributing
Feel free to submit **pull requests** or **report issues** to improve the project!

## 🌟 Acknowledgments
Special thanks to the **YouTube API team** and **Streamlit community** for making this project possible!

