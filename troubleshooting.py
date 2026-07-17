from google import genai
import os
from dotenv import load_dotenv

# Load your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env")
    exit()

client = genai.Client(api_key=api_key)

print("--- Fetching models available to your API Key ---")
try:
    # This lists the models directly from the API
    models = client.models.list()
    for m in models:
        # We only want models you can actually chat with
        print(f"✅ Available Model Name: {m.name}")
except Exception as e:
    print(f"❌ Failed to list models: {e}")