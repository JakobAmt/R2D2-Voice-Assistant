import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# --- ElevenLabs ---
ELEVENLABS_VOICE_ID = "XrExE9yKIg1WjnnlVkGX"
ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"
ELEVENLABS_OUTPUT_FORMAT = "mp3_44100_128"

# --- Gemini ---
GEMINI_MODEL = "gemini-2.0-flash"

# --- GPIO Pins ---
BLUE_LED = 12
RED_LED = 13

# --- Weather API Settings ---
WEATHER_CITY = "Oslo"
WEATHER_UNITS = "metric"

# --- Wake Word ---
WAKE_WORD = "hey r2"

# --- R2D2 Sounds ---
SOUNDS_FOLDER = "/home/jakob/Desktop/r2d2/R2 sounds/"
SOUNDS = [
    f"{SOUNDS_FOLDER}004 gen-4.mp3",
    f"{SOUNDS_FOLDER}007 gen-7.mp3",
    f"{SOUNDS_FOLDER}008 gen-8.mp3",
]

# --- System prompt ---
SYSTEM_INSTRUCTION = (
    "You are R2D2, a concise and friendly AI voice assistant. "
    "Respond conversationally without markdown or symbols. "
    "Keep answers short and direct."
)