import streamlit as st
import os
from youtube_backend import (
    process_excel,
    export_playlist_to_excel,
    authenticate_youtube,
    merge_playlists_auto
)

st.set_page_config(page_title="YouTube Playlist Manager", layout="centered")

st.title("🎵 YouTube Playlist Manager")
st.write("Manage your YouTube playlists by merging, exporting, or creating new ones!")

# Authenticate YouTube API once and reuse it
youtube = authenticate_youtube()

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["🔀 Merge Playlists", "📂 Create Playlist", "📥 Export Playlist"])

with tab1:
    st.header("Merge YouTube Playlists")

    playlist_urls = st.text_area(
        "Enter YouTube Playlist URLs (one per line)",
        placeholder="https://www.youtube.com/playlist?list=...\nhttps://www.youtube.com/playlist?list=..."
    )

    new_playlist_name = st.text_input("Enter New Playlist Name", placeholder="My Merged Playlist")
    new_playlist_description = st.text_area("Enter Playlist Description", placeholder="A combined playlist")

    if st.button("🔄 Auto Merge"):
        urls = [url.strip() for url in playlist_urls.split("\n") if url.strip()]
        if len(urls) < 2:
            st.error("Please enter at least two valid playlist URLs!")
        elif not new_playlist_name:
            st.error("Please enter a name for the new playlist!")
        else:
            result = merge_playlists_auto(youtube, playlist_urls=urls, new_playlist_name=new_playlist_name,
                                          new_playlist_description=new_playlist_description)
            st.success(result)
with tab2:
    st.header("Create a YouTube Playlist from Excel")

    playlist_name = st.text_input("Enter Playlist Name", placeholder="My Playlist")
    playlist_description = st.text_area("Enter Playlist Description", placeholder="A collection of videos")

    uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type=["xlsx"])

    if st.button("Create Playlist"):
        if not playlist_name:
            st.error("Please enter a playlist name!")
        elif not uploaded_file:
            st.error("Please upload an Excel file!")
        else:
            result = process_excel(uploaded_file, playlist_name, playlist_description)
            st.success(result)

with tab3:
    st.header("Export a YouTube Playlist to Excel")

    playlist_url = st.text_input("Enter YouTube Playlist URL", placeholder="https://www.youtube.com/playlist?list=...")

    if st.button("Export Playlist"):
        if not playlist_url:
            st.error("Please enter a playlist URL!")
        else:
            output_path = "exports/playlist_videos.xlsx"
            os.makedirs("exports", exist_ok=True)

            result = export_playlist_to_excel(youtube, playlist_url, output_path)
            if "exported" in result:
                with open(output_path, "rb") as f:
                    st.download_button(label="📥 Download Excel File", data=f, file_name="playlist_videos.xlsx")
                st.success("Playlist exported successfully!")
            else:
                st.error(result)
