import streamlit as st
import requests
import openai
from openai import OpenAI
import io
import os

# Get the API key from Streamlit secrets or environment variable
if os.getenv("OPENAI_API_KEY"):
    openai_api_key = os.getenv("OPENAI_API_KEY")
else:
    openai_api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=openai_api_key)

def speech_to_text(audio_file):
    # Save the uploaded audio file to a temporary WAV file
    temp_file_path = "temp_audio.wav"
    with open(temp_file_path, "wb") as f:
        f.write(audio_file.getvalue())

    # Use the OpenAI Whisper API to transcribe the audio
    with open(temp_file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    # Access the transcription text as an attribute
    st.write("Transcript:", transcription.text)
    return transcription.text


def describe_image(image_url):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Describe this image like an IELTS exam: {image_url}"
        }]
    )
    st.write("Chat GPT:", response.choices[0].message.content)
    return response.choices[0].message.content

def compare_descriptions(model_desc, user_desc):
    st.write(f" Description: {model_desc}")
    st.write(f"Your Description: {user_desc}")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": "You are a language teacher. You will provide feedback on grammar and vocabulary for the user-provided description of an image."
        }, {
            "role": "user",
            "content": f"Model description: {model_desc}. User description: {user_desc}. Provide feedback on the user's description."
        }]
    )
    st.subheader('Feedback')
    print(completion.choices[0].message.content)
    st.write(f"Analysis: {completion.choices[0].message.content}")

def app():
    st.header('Image Comprehension')
    st.write('Learn to understand and describe images in your target language. This task focuses on improving your speaking skills and vocabulary.')

    if 'image_shown' not in st.session_state:
        st.session_state.image_shown = False
    if 'recording_started' not in st.session_state:
        st.session_state.recording_started = False

    # Start button to display the image
    if st.button('Start'):
        st.session_state.image_shown = True
        st.session_state.image_generated = False

    if st.session_state.image_shown:
        # Display the image
        if not st.session_state.image_generated:
            url = "https://picsum.photos/1280/720"
            response = requests.get(url)
            image_url = response.url
            st.session_state.image_url = image_url
            st.session_state.image_generated = True
        st.image(st.session_state.image_url, caption="Describe this image")

        st.subheader("Click on mic button below and record your description. Focus on fluency and rich description.")

        # Record audio using st.audio_input
        audio_value = st.audio_input(label="Record your description", disabled=False)

        if audio_value:
            # When audio is recorded, process it
            st.write("Audio recorded, processing now...")
            user_description = speech_to_text(audio_value)

            # Get model description of the image
            model_description = describe_image(st.session_state.image_url)

            # Compare descriptions and provide feedback
            compare_descriptions(model_description, user_description)

# Uncomment the following line to run the app
# if __name__ == "__main__":
#     app()
