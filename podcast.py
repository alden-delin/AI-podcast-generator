import os
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

# --- CONFIGURATION ---
# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- STAGE 1: SCRIPT GENERATION ---
def generate_podcast_script(topic):
    """Generates a podcast script using the Gemini API."""
    print(f"🎙️ Generating podcast script for topic: {topic}...")
    
    # Configure the generative model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create a detailed prompt for the AI
    prompt = f"""
    You are a podcast host. Generate a short, engaging, and informative podcast script about '{topic}'.
    The script should be around 300 words.
    Structure it with a brief intro, a main body with 2-3 key points, and a concluding outro.
    The tone should be conversational and easy to understand.
    Just provide the raw text for the host to speak.
    """
    
    try:
        response = model.generate_content(prompt)
        print("✅ Script generated successfully!")
        return response.text
    except Exception as e:
        print(f"Error generating script: {e}")
        return None

# --- STAGE 2: TEXT-TO-SPEECH (TTS) ---
def create_audio_from_text(script_text, output_filename="podcast_episode.mp3"):
    """Converts the script text to an MP3 audio file."""
    print("🔊 Converting script text to speech...")
    try:
        tts = gTTS(text=script_text, lang='en', slow=False)
        tts.save(output_filename)
        print(f"✅ Your podcast is ready! Saved to {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Error during Text-to-Speech: {e}")
        return None

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Define the topic for your podcast episode
    podcast_topic = "the surprising history of coffee"

    # --- Run the simplified pipeline ---
    # 1. Generate script
    script = generate_podcast_script(podcast_topic)
    
    if script:
        # 2. Convert script to the final audio file
        create_audio_from_text(script)