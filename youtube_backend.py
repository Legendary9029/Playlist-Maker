import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from urllib.parse import urlparse, parse_qs
import streamlit as st

# OAuth YouTube API settings
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CLIENT_SECRETS_FILE = 'client_secret.json'


def authenticate_youtube():
    """Authenticate and return a YouTube API client."""
    creds = None
    token_file = "token.json"

    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception as e:
            print(f"Error loading token.json: {e}")
            os.remove(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                print("Token refresh failed, re-authenticating...")
                creds = None

        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w") as token_file:
            token_file.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def create_playlist(youtube, title, description):
    """Create a new YouTube playlist and return its ID."""
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "defaultLanguage": "en"},
            "status": {"privacyStatus": "public"}
        }
    )
    response = request.execute()
    return response["id"]


def add_video_to_playlist(youtube, playlist_id, video_id):
    """Add a video to the specified playlist by video ID."""
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id}
            }
        }
    ).execute()


def extract_video_id(url):
    """Extracts a playlist ID or video ID from a YouTube URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if "list" in query_params:
        return query_params["list"][0]  # Returns Playlist ID
    elif "v" in query_params:
        return query_params["v"][0]  # Returns Video ID
    elif parsed_url.hostname in ["youtu.be", "www.youtu.be"]:
        return parsed_url.path.lstrip("/")
    return None



def get_playlist_videos(youtube, playlist_id):
    """Retrieve all video IDs from a YouTube playlist."""
    video_ids = []
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    while request:
        response = request.execute()
        if "items" not in response:
            print(f"⚠️ No videos found in playlist {playlist_id} (check privacy settings).")
            return []

        for item in response.get("items", []):
            video_ids.append({
                "Title": item["snippet"]["title"],
                "Video ID": item["snippet"]["resourceId"]["videoId"],
                "Video URL": f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
            })
        request = youtube.playlistItems().list_next(request, response)

    if not video_ids:
        print(f"⚠️ Playlist {playlist_id} is empty or private.")
    return video_ids

def process_excel(uploaded_file, playlist_name, playlist_description):
    """Process an Excel file and add videos to the created playlist."""
    df = pd.read_excel(uploaded_file)
    if 'URL' not in df.columns:
        return "Error: The Excel file must contain a 'URL' column."

    youtube = authenticate_youtube()
    playlist_id = create_playlist(youtube, playlist_name, playlist_description)

    urls = df['URL'].dropna().astype(str).tolist()
    for url in urls:
        video_id = extract_video_id(url)
        if video_id:
            add_video_to_playlist(youtube, playlist_id, video_id)

    return f"✅ Playlist '{playlist_name}' created successfully!"


def export_playlist_to_excel(youtube, playlist_url, output_path="merged_playlist.xlsx"):
    """Export a YouTube playlist's videos to an Excel file."""
    playlist_id = extract_video_id(playlist_url)
    if not playlist_id:
        return "Error: Invalid playlist URL."

    videos = get_playlist_videos(youtube, playlist_id)
    if not videos:
        return "No videos to export."

    df = pd.DataFrame(videos)
    df.to_excel(output_path, index=False)
    return f"✅ Playlist exported to {output_path}"


def merge_playlists(youtube, playlist_urls, new_playlist_name, new_playlist_description, manual_selection=False):
    """
    Merge multiple playlists into a new one with a progress bar (Streamlit version).
    """
    st.header("Merge YouTube Playlists")

    # User input for playlist URLs
    playlist_urls = st.text_area("Enter YouTube playlist URLs (one per line):").strip().split("\n")
    playlist_urls = [url.strip() for url in playlist_urls if url.strip() and "playlist?list=" in url]

    if st.button("Merge Playlists"):
        if not playlist_urls:
            st.error("No valid playlists provided. Operation cancelled.")
            return

        video_list = []
        valid_playlists = []

        for playlist_url in playlist_urls:
            playlist_id = extract_video_id(playlist_url)
            if not playlist_id:
                st.warning(f"⚠️ Skipping invalid playlist URL: {playlist_url}")
                continue

            videos = get_playlist_videos(youtube, playlist_id)
            if not videos:
                st.warning(f"⚠️ Skipping empty/private playlist: {playlist_url}")
                continue

            video_list.extend(videos)
            valid_playlists.append({"id": playlist_id, "url": playlist_url, "videos": videos})

        if not valid_playlists:
            st.error("No accessible playlists found. Check URLs and try again.")
            return

        # Manual selection option
        if manual_selection:
            st.subheader("✅ Select Videos to Add to the New Playlist")
            selected_videos = []
            for video in video_list:
                if st.checkbox(f"{video['Title']} ({video['Video URL']})", key=video["Video ID"]):
                    selected_videos.append(video)
            video_list = selected_videos if selected_videos else video_list

        # Create new playlist
        new_playlist_id = create_playlist(youtube, new_playlist_name, new_playlist_description)

        # Progress bar
        progress_bar = st.progress(0)
        for i, video in enumerate(video_list):
            add_video_to_playlist(youtube, new_playlist_id, video["Video ID"])
            progress_bar.progress((i + 1) / len(video_list))

        # Export merged playlist
        export_playlist_to_excel(video_list)

        st.success(f"✅ New playlist '{new_playlist_name}' created with {len(video_list)} videos!")
