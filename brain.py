import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_INSTRUCTION

# --- Initialize Gemini ---
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(GEMINI_MODEL)

# --- Start chat session ---
def new_chat_session():
    return gemini_model.start_chat(
        history=[{"role": "user", "parts": [SYSTEM_INSTRUCTION]}]
    )

gemini_chat = new_chat_session()

# --- Get response ---
def get_gemini_response(prompt):
    try:
        response = gemini_chat.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return "I'm having trouble thinking right now."

# --- Reset memory ---
def reset_chat():
    global gemini_chat
    gemini_chat = new_chat_session()
    print("Chat memory reset.")