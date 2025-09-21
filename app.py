import os
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

# --- INITIAL CONFIGURATION ---
# Set page configuration for a cleaner look
st.set_page_config(
    page_title="AI Podcast Generator",
    page_icon="🎙️",
    layout="wide"
)

# Load API Key
load_dotenv()
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except AttributeError:
    st.error("🚨 Google API Key not found! Please make sure it's in your .env file.")
    st.stop()


# --- BACKEND FUNCTIONS (with Streamlit caching) ---

@st.cache_data(show_spinner="✍️ Generating podcast script...")
def generate_podcast_script(topic):
    """Generates a podcast script using the Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are a podcast host. Generate a short, engaging, and informative podcast script about '{topic}'.
    The script should be around 300 words.
    Structure it with a brief intro, a main body with 2-3 key points, and a concluding outro.
    The tone should be conversational and easy to understand.
    Just provide the raw text for the host to speak.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred during script generation: {e}")
        return None

@st.cache_data(show_spinner="🎤 Converting script to audio...")
def create_audio_from_text(script_text, filename):
    """Converts the script text to an MP3 audio file."""
    try:
        tts = gTTS(text=script_text, lang='en', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"An error occurred during audio creation: {e}")
        return None

# --- STREAMLIT UI ---

# Title and Description
st.title("🎙️ AI Podcast Generator")
st.markdown("Turn any topic into a short, listenable podcast episode in seconds. Powered by Google Gemini and gTTS.")

st.divider()

# Input field for the podcast topic
topic_input = st.text_input(
    "Enter the topic for your podcast:",
    placeholder="e.g., The future of renewable energy"
)

# Generate button
if st.button("✨ Generate Podcast"):
    if not topic_input:
        st.warning("Please enter a topic to generate the podcast.")
    else:
        # --- Generation Pipeline ---
        script = generate_podcast_script(topic_input)
        
        if script:
            audio_filename = f"podcast_{topic_input.replace(' ', '_')[:20]}.mp3"
            audio_file_path = create_audio_from_text(script, audio_filename)
            
            if audio_file_path:
                st.success("Your podcast has been successfully generated!")

                # Display the generated script in an expandable section
                with st.expander("📖 View Podcast Script"):
                    st.write(script)

                # Display the audio player
                st.audio(audio_file_path, format='audio/mp3')

                # Provide a download button
                with open(audio_file_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Podcast (MP3)",
                        data=file,
                        file_name=audio_filename,
                        mime="audio/mp3"
                    )
                
                # Store the file path in session state to persist it
                st.session_state.audio_file = audio_file_path