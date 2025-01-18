import streamlit as st
import requests
import numpy as np
import wave
import openai
import os
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, Mode
from io import BytesIO

# OpenAI API Key setup
if os.getenv("OPENAI_API_KEY"):
    openai_api_key = os.getenv("OPENAI_API_KEY")
else:
    openai_api_key = st.secrets["OPENAI_API_KEY"]

client = openai

# Check if the webrtc context and the audio receiver exist
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame):
        # Append each audio frame for later processing
        self.frames.append(frame)
        return frame

    def get_audio(self):
        # Combine all frames into a single audio file
        audio = np.concatenate([f.to_ndarray() for f in self.frames], axis=0)
        return audio

# Function to convert speech to text
def speech_to_text(audio_data):
    # Create a temporary audio file to send to OpenAI API
    with BytesIO() as byte_io:
        write(byte_io, 44100, audio_data)  # 44100 is the sample rate used
        byte_io.seek(0)  # Reset buffer to start

        audio_file = openai.Audio.create(
            file=byte_io,
            model="whisper-1"
        )
        return audio_file['text']

# Function to describe the image (existing)
def describe_image(image_url):
    response = client.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Describe this image like an IELTS exam: {image_url}"
        }]
    )
    return response['choices'][0]['message']['content']

# Compare the model and user description (existing)
def compare_descriptions(model_desc, user_desc):
    completion = client.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": "You are a language teacher. You will provide feedback on grammar and vocabulary for the user-provided description of an image."
        }, {
            "role": "user",
            "content": f"Model description: {model_desc}. User description: {user_desc}. Provide feedback on the user's description."
        }]
    )
    return completion['choices'][0]['message']['content']

# Streamlit App Logic
def app():
    st.title("Image Comprehension")
    st.write('Learn to describe and analyze images in your target language. This task will help you improve your speaking skills.')

    if 'image_shown' not in st.session_state:
        st.session_state.image_shown = False
    if 'recording_started' not in st.session_state:
        st.session_state.recording_started = False

    if st.button("Start"):
        st.session_state.image_shown = True
        st.session_state.image_generated = False

    if st.session_state.image_shown:
        if not st.session_state.image_generated:
            url = "https://picsum.photos/1280/720"
            response = requests.get(url)
            image_url = response.url
            st.session_state.image_url = image_url
            st.session_state.image_generated = True
        st.image(st.session_state.image_url, caption="Describe this image")

        st.subheader("You have 30 seconds to describe the image. Focus on fluency and rich description.")

        # Fixing the mode issue here
        webrtc_ctx = webrtc_streamer(
            key="audio-recorder",
            mode=Mode.SENDRECV,  # Using enum instead of string
            audio_processor_factory=AudioProcessor,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"audio": True, "video": False}
        )

        if webrtc_ctx.audio_receiver:
            audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            if audio_frames:
                st.write(f"Recording completed with {len(audio_frames)} audio frames.")
                audio_data = webrtc_ctx.audio_receiver.get_audio()
                user_description = speech_to_text(audio_data)
                st.write(f"Your transcription: {user_description}")

                model_description = describe_image(st.session_state.image_url)
                st.write(f"Model description: {model_description}")

                feedback = compare_descriptions(model_description, user_description)
                st.subheader('Feedback')
                st.write(feedback)

if __name__ == "__main__":
    app()
