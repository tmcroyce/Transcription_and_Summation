import streamlit as st
from moviepy.editor import *
import tempfile
import os

# Title of the Streamlit app
st.title('MP4 to MP3 Converter')

# File uploader allows user to add their own video
uploaded_file = st.file_uploader("Upload MP4 file", type="mp4")

if uploaded_file is not None:
    # Display a message
    st.text("Converting...")

    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(uploaded_file.read())
        tmpfile_path = tmpfile.name

    # Load the video file from the temporary path
    video = VideoFileClip(tmpfile_path)

    # Extract the audio
    audio = video.audio

    # Create a temporary file for the audio output
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpoutfile:
        audio_output_path = tmpoutfile.name

    # Write the audio file to the temporary output file
    audio.write_audiofile(audio_output_path)

    # Read the temporary audio file into a BytesIO object
    mp3_buffer = BytesIO()
    with open(audio_output_path, "rb") as f:
        mp3_buffer.write(f.read())
    mp3_buffer.seek(0)

    # Close the video file to release resources
    video.close()

    # Delete the temporary video file
    os.unlink(tmpfile_path)

    # Delete the temporary audio file
    os.unlink(audio_output_path)

    # Provide a download button to download the MP3 file
    st.download_button(
        label="Download MP3",
        data=mp3_buffer,
        file_name="converted_audio.mp3",
        mime="audio/mp3"
    )

    # Display a success message
    st.success("Conversion successful!")