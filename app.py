from deepgram import Deepgram
import streamlit as st
import base64
import openai
st.set_page_config(page_title='Audio Transcription & Summation', page_icon=None, layout="wide", initial_sidebar_state="auto" )

# Setup CSS Button Class
st.markdown("""
<style>
.custom-button {
    display: inline-block;
    padding: 0.5em 1.5em;
    text-decoration: none;
    color: #fff;
    background-color: #167A74;
    font-weight: bold;
    text-align: center;
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
    border-radius: 20px;
    cursor: pointer;
}
.custom-button:hover {
    background-color: #1d9078;
}
</style>
""", unsafe_allow_html=True)

def get_image_base64_string(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def set_background_image(image_path):
    image_base64_string = get_image_base64_string(image_path)
    st.markdown(f"""
        <style>
        body {{
            background-image: url("data:image/png;base64,{image_base64_string}");
            background-size: cover;
        }}
        </style>
    """, unsafe_allow_html=True)

# Example usage
image_path = "photos/backg.png"  # Path to your background image
set_background_image(image_path)

st.image(image_path, caption='Background Image')


# Setup Deepgram
api_key = st.secrets['deepgram_api']
client = Deepgram(api_key)

# Setup OpenAI
openai.api_key = st.secrets['openAI_API_Key']

# User Session State Setup
def get_user_session_state():
    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = {}
    return st.session_state['session_state']

#API Call
def process_code(user_code):
    # Define the OpenAI API request
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful interview summarizer."},
            {"role": "user", "content": "This is an interview I need summarized: \n\n" + user_code + "\n\n Summarize the interview in bullet-point and sub-bullet-point format."},
        ]
    )

    # Get the response from the OpenAI API
    result = response['choices'][0]['message']['content']
    return result

# Set Title
st.markdown(f"""
    <h1 style="
        font-family: Arial, sans-serif;
        font-size: 48px;
        font-weight: bold;
        color: #167A74;
        text-align: center;
        padding: 10px;
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Add 3D shadow effect */
        border-radius: 20px;
    ">Audio Transcription & Summation</h1>
""", unsafe_allow_html=True)

st.subheader("")

# Create DL Link Function
def create_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href


#Upload audio file
uploaded_file = st.file_uploader("Choose an MP3 audio file to upload", type="mp3")

user_session_state = get_user_session_state()



if uploaded_file is not None:
    # add a transcribe button
    if st.button('Transcribe Audio'):
        st.markdown("""
            <h2 style="
                    font-family: Arial, sans-serif;
                    font-size: 20px;
                    font-weight: bold;
                    color: #167A74; 
                    text-align: center;
                    padding: 10px;
                    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Add 3D shadow effect */
                    border-radius: 30px;;
                ">Audio Transcription in Progress...</h2>
                
            """, unsafe_allow_html=True)        
        audio_file = uploaded_file.read()
        # set options
        options = {
            "punctuate": True,
            "model": 'general',
            "tier": 'enhanced',
            "punctuate": True,
            "speaker_labels": True,  # Enable speaker identification
            "diarize": True,  # Enable speaker identification
            "paragraphs": True,
        }
        # Transcribe the audio file and enable speaker identification

        source = {"buffer": audio_file, "mimetype": 'audio/mp3'}
        response = client.transcription.sync_prerecorded(source, options)


        user_session_state['new_transcript'] = response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']
        # save transcript to a variable, show in box


    # check if new_transcript is a variable


    if 'new_transcript' in user_session_state:
        st.markdown("""
            <h2 style="
                    font-family: Arial, sans-serif;
                    font-size: 20px;
                    font-weight: bold;
                    color: #167A74;
                    text-align: center;
                    padding: 10px;
                    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Add 3D shadow effect */
                    border-radius: 30px;;
                ">...Transcription Complete!</h2>
                
            """, unsafe_allow_html=True)
        
        st.write('')

        # add button to download transcript
        st.download_button(
            label="Download Transcript",
            data=user_session_state['new_transcript'].encode(),
            file_name="transcript.txt",
            mime="text/plain"
        )
        st.write('')
    else: 
        pass

    if 'new_transcript' in user_session_state:
        if st.button('Read Transcript'):
            st.write(user_session_state['new_transcript'])

    if 'new_transcript' in user_session_state:
        if st.button('Summarize Transcript'):
            st.write('This could take a moment, as it utilizes the OpenAI GPT-4 API due to its ability to handle long-form text...')
            user_session_state['transcript_summary']= process_code(user_session_state['new_transcript'])
        
    if 'transcript_summary' in user_session_state:
            st.markdown("""
            <h2 style="
                    font-family: Arial, sans-serif;
                    font-size: 20px;
                    font-weight: bold;
                    color: #167A74;
                    text-align: center;
                    padding: 10px;
                    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Add 3D shadow effect */
                    border-radius: 30px;;
                ">...Summary Complete!</h2>
                
            """, unsafe_allow_html=True)
            st.write('')


            # add button to download summary
            st.download_button(
                label="Download Transcript Summary",
                data=user_session_state['transcript_summary'].encode(),
                file_name="summary.txt",
                mime="text/plain"
            )

            markdown_variable = user_session_state['transcript_summary']
            
            # Define a unique ID for the custom Markdown
            markdown_id = "custom-markdown-id"

            
            # Display the Markdown in Streamlit using the unique ID
            st.markdown(f'<div id="{markdown_id}">{markdown_variable}</div>', unsafe_allow_html=True)

            # Define the CSS rules for the custom ID
            css_rules = f"""
            <style>
            #{markdown_id} {{
            display: block;
            color: #1d9078;
            font-weight: bold;
            padding: 10px;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
            border-radius: 20px;
            }}
            </style>
            """

            # Apply the CSS rules in Streamlit
            st.markdown(css_rules, unsafe_allow_html=True)
# # add CSS for stMarkdownContainer
# st.markdown("""
# <style>
# [data-testid="stMarkdownContainer"] {
#         color: #167A74;
#         text-align: center;
#         font-weight: bold;
#         padding: 10px;
#         box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Add 3D shadow effect */
#         border-radius: 20px;
#         }
#         </style>
#         """, unsafe_allow_html=True)
