import pandas as pd
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from urllib.parse import urlparse, parse_qs

# Path to the Excel file with YouTube links
excel_file_path = 'links.xlsx'

# OAuth scopes and credentials
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CLIENT_SECRETS_FILE = 'client_secret.json'

def authenticate_youtube():
    """Authenticate and return a YouTube API client."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())
    youtube = build("youtube", "v3", credentials=creds)
    return youtube

def create_playlist(youtube, title, description):
    """Create a new YouTube playlist and return its ID."""
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "public"
            }
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
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()

def extract_video_id(url):
    """Extract the YouTube video ID from the URL."""
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['youtu.be']:
            return parsed_url.path.lstrip('/')
        elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed_url.path == '/watch':
                query_params = parse_qs(parsed_url.query)
                return query_params.get('v', [None])[0]
            elif parsed_url.path.startswith('/embed/'):
                return parsed_url.path.split('/')[2]
            elif parsed_url.path.startswith('/v/'):
                return parsed_url.path.split('/')[2]
        # Handle other possible YouTube URL formats if necessary
    except Exception as e:
        print(f"Error parsing URL '{url}': {e}")
    return None

def main():
    # Get playlist details from the user
    title = input("Enter the playlist name: ")
    description = input("Enter the playlist description: ")

    # Authenticate with YouTube API
    youtube = authenticate_youtube()

    # Create a new playlist
    playlist_id = create_playlist(youtube, title=title, description=description)

    # Read the Excel file and get video URLs
    try:
        df = pd.read_excel(excel_file_path)
    except FileNotFoundError:
        print(f"Error: The file '{excel_file_path}' was not found.")
        return
    except Exception as e:
        print(f"Error reading '{excel_file_path}': {e}")
        return

    if 'URL' not in df.columns:
        print("Error: The Excel file does not contain a 'URL' column.")
        return

    urls = df['URL'].dropna().tolist()

    if not urls:
        print("No URLs found in the Excel file.")
        return

    # Add each video to the playlist
    for idx, url in enumerate(urls, start=1):
        video_id = extract_video_id(url)
        if video_id:
            try:
                add_video_to_playlist(youtube, playlist_id, video_id)
                print(f"[{idx}/{len(urls)}] Added video ID: {video_id}")
            except Exception as e:
                print(f"[{idx}/{len(urls)}] Failed to add video ID '{video_id}': {e}")
        else:
            print(f"[{idx}/{len(urls)}] Invalid URL format or missing video ID: '{url}'")

    print("Playlist creation process completed.")

if __name__ == "__main__":
    main()
