import streamlit as st
from pytube import YouTube
import os
import time
from tempfile import NamedTemporaryFile, gettempdir

def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if stream:
        # Save the video to a temporary file
        temp_file = NamedTemporaryFile(delete=False, suffix='.mp4')
        stream.download(filename=temp_file.name)
        return temp_file.name
    return None

def cleanup_old_files(directory, file_extension='.mp4', age_limit_seconds=20):
    """Deletes files with a specific extension and older than 'age_limit_seconds' in the given directory."""
    current_time = time.time()
    for filename in os.listdir(directory):
        if filename.endswith(file_extension):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and current_time - os.path.getmtime(file_path) > age_limit_seconds:
                os.remove(file_path)

def main():
    st.title('YouTube Video Downloader')
    st.text('by Helio Nogueira Cardoso')
    url = st.text_input('Enter YouTube URL')
    if st.button('Download'):
        filepath = download_video(url)
        if filepath:
            st.success('Download successful! Click below to download the video to your device.')
            # Provide a link for the user to download the video
            with open(filepath, "rb") as file:
                btn = st.download_button(
                    label="Download Video",
                    data=file,
                    file_name="downloaded_video.mp4",
                    mime="video/mp4"
                )
            # Schedule a cleanup for old files
            cleanup_old_files(gettempdir())
        else:
            st.error('Download failed. Check the URL and try again.')

if __name__ == '__main__':
    main()