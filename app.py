import streamlit as st
import os
from backend import process_excel, export_playlist_to_excel, authenticate_youtube

st.set_page_config(page_title="YouTube Playlist Manager", layout="centered")

st.title("🎵 YouTube Playlist Manager")
st.write("Upload an Excel file to create a YouTube playlist or enter a YouTube playlist URL to export it.")

# Tabs for different functionalities
tab1, tab2 = st.tabs(["📂 Create Playlist", "📥 Export Playlist"])

with tab1:
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
            file_path = os.path.join("uploads", uploaded_file.name)
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            result = process_excel(file_path, playlist_name, playlist_description)
            st.success(result)

with tab2:
    st.header("Export a YouTube Playlist to Excel")

    playlist_url = st.text_input("Enter YouTube Playlist URL", placeholder="https://www.youtube.com/playlist?list=...")

    if st.button("Export Playlist"):
        if not playlist_url:
            st.error("Please enter a playlist URL!")
        else:
            youtube = authenticate_youtube()
            output_path = "exports/playlist_videos.xlsx"
            os.makedirs("exports", exist_ok=True)

            result = export_playlist_to_excel(playlist_url, output_path)
            if "exported" in result:
                with open(output_path, "rb") as f:
                    st.download_button(label="📥 Download Excel File", data=f, file_name="playlist_videos.xlsx")
                st.success("Playlist exported successfully!")
            else:
                st.error(result)
