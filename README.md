# Audio Transcription & Summation
This Python script uses Deepgram and OpenAI GPT-4 to transcribe and summarize uploaded audio files. It provides a user-friendly interface using the Streamlit library.

## Requirements
- Python 3.6 or higher
- deepgram-sdk
- openai
- streamlit

## To install the required libraries, run:

```python
pip install deepgram-sdk openai streamlit
```

## Usage
Set up your API keys for Deepgram and OpenAI by adding them to a secrets.toml file in your working directory. The format should be:
- toml
```
deepgram_api = "your_deepgram_api_key"
openAI_API_Key = "your_openai_api_key"
```
Run the script using Streamlit:
```
streamlit run script_name.py
```

- Navigate to the provided URL in your web browser.
- Upload an MP3 audio file.
- Click "Transcribe Audio" to transcribe the uploaded audio file using Deepgram's API. The transcription will be displayed and can be downloaded as a plain text file.
- Click "Read Transcript" to display the full transcription on the screen.
- Click "Summarize Transcript" to create a summary of the transcript using OpenAI's GPT-4 API. The summary will be displayed in bullet-point and sub-bullet-point format and can be downloaded as a plain text file.

## Features
- Upload and process MP3 audio files
- Transcribe audio using Deepgram's API
- Summarize transcriptions using OpenAI's GPT-4 API
- Display and download transcriptions and summaries in plain text format

## Customization
This script is easily customizable with different formatting and styles. You can modify the CSS rules in the st.markdown sections to change the appearance of the page, buttons, and other elements.
