import pygame
import tempfile
import os
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, ELEVENLABS_MODEL_ID, ELEVENLABS_OUTPUT_FORMAT

# --- Initialize ElevenLabs ---
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# --- Play audio file ---
def play_audio_file(file_path):
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"Audio playback error: {e}")
    finally:
        pygame.mixer.quit()

# --- Speak text via ElevenLabs ---
def speak_text(text):
    print(f"R2D2: '{text}'")
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            audio_stream = elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=ELEVENLABS_VOICE_ID,
                model_id=ELEVENLABS_MODEL_ID,
                output_format=ELEVENLABS_OUTPUT_FORMAT,
            )
            for chunk in audio_stream:
                if chunk:
                    temp_audio_file.write(chunk)
            temp_file_path = temp_audio_file.name

        play_audio_file(temp_file_path)
    except Exception as e:
        print(f"Error generating or playing audio: {e}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)