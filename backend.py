import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from urllib.parse import urlparse, parse_qs

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
            os.remove(token_file)  # Delete corrupted token file

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())  # Try refreshing token
            except Exception:
                print("Token refresh failed, re-authenticating...")
                creds = None  # Force re-authentication

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
    return request.execute()["id"]

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
    """Extract video ID from a YouTube URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if "list" in query_params:
        return query_params["list"][0]  # Playlist ID
    elif "v" in query_params:
        return query_params["v"][0]  # Single video ID
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")
    return None

def get_playlist_videos(youtube, playlist_id):
    """Retrieve all video IDs from a YouTube playlist."""
    video_ids = []
    request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=50)
    while request:
        response = request.execute()
        for item in response.get("items", []):
            video_ids.append({
                "Title": item["snippet"]["title"],
                "Video URL": f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
            })
        request = youtube.playlistItems().list_next(request, response)
    return video_ids

def process_excel(file_path, playlist_name, playlist_description):
    """Process an Excel file and add videos to the created playlist."""
    df = pd.read_excel(file_path)
    if 'URL' not in df.columns:
        return "Error: The Excel file must contain a 'URL' column."

    youtube = authenticate_youtube()
    playlist_id = create_playlist(youtube, playlist_name, playlist_description)

    urls = df['URL'].dropna().astype(str).tolist()
    for url in urls:
        video_id = extract_video_id(url)
        if video_id:
            add_video_to_playlist(youtube, playlist_id, video_id)

    return f"Playlist '{playlist_name}' created successfully!"

def export_playlist_to_excel(playlist_url, output_path):
    """Export a YouTube playlist to an Excel file."""
    youtube = authenticate_youtube()
    playlist_id = extract_video_id(playlist_url)
    if not playlist_id:
        return "Invalid playlist URL."

    video_list = get_playlist_videos(youtube, playlist_id)
    if not video_list:
        return "No videos found in the playlist."

    df = pd.DataFrame(video_list)
    df.to_excel(output_path, index=False)
    return f"Playlist exported to {output_path}"
