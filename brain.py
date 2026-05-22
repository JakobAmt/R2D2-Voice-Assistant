from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_INSTRUCTION

# --- Initialize Gemini ---
client = genai.Client(api_key=GEMINI_API_KEY)

# --- Chat history ---
chat_history = []

# --- Get response ---
def get_gemini_response(prompt):
    global chat_history
    try:
        chat_history.append({"role": "user", "parts": [{"text": prompt}]})
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=chat_history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
            )
        )
        
        reply = response.text
        chat_history.append({"role": "model", "parts": [{"text": reply}]})
        return reply
    except Exception as e:
        print(f"Gemini error: {e}")
        return "I'm having trouble thinking right now."

# --- Reset memory ---
def reset_chat():
    global chat_history
    chat_history = []
    print("Chat memory reset.")