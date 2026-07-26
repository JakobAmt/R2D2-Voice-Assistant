import speech_recognition as sr
import random
from audio import speak_text, play_audio_file
from led import start_blue_fade, stop_blue_fade, red_led_on, red_led_off
from brain import get_gemini_response, reset_chat
from config import SOUNDS, WAKE_WORD
from skills import weather
from skills.timer import get_time, get_date
from state import add_to_history, set_status, reset_history


def extract_city(text):
    """Try to extract a city name from the command."""
    # Common trigger phrases
    triggers = [
        "weather in ",
        "weather for ",
        "weather at ",
        "temperature in ",
        "temperature at ",
        "what's the weather in ",
        "what is the weather in ",
        "how is the weather in ",
        "how's the weather in ",
    ]
    text_lower = text.lower()
    for trigger in triggers:
        if trigger in text_lower:
            # Extract everything after the trigger
            city = text_lower.split(trigger)[-1].strip()
            # Clean up common endings
            for ending in [" today", " now", " like", " right now", "?"]:
                city = city.replace(ending, "")
            return city.strip().title()
    return None

# --- Intent routing ---
def route_command(text):
    if any(w in text for w in ["weather", "temperature", "rain", "forecast"]):
        city = extract_city(text)
        return weather.get_weather(city)  # None = use default
    elif any(w in text for w in ["time", "clock"]):
        return timer.get_time()
    elif any(w in text for w in ["date", "day", "today"]):
        return timer.get_date()
    else:
        return get_gemini_response(text)




# --- Command processor ---
def command_processor():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for command...")
        red_led_off()
        start_blue_fade()
        set_status("listening")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=8)
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: '{text}'")

            stop_blue_fade()
            red_led_on()
            set_status("processing")
            add_to_history("user", text)

            if "thanks r2" in text or "thank you r2" in text:
                speak_text("Always! I'm here to help.")
                reset_chat()
                reset_history()
                start_blue_fade()
                red_led_off()
                set_status("standby")
                return "END_CONVERSATION"

            response = route_command(text)
            set_status("speaking")
            add_to_history("assistant", response)
            speak_text(response)
            set_status("listening")

        except sr.WaitTimeoutError:
            stop_blue_fade()
            set_status("standby")
            speak_text("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            stop_blue_fade()
            set_status("standby")
            speak_text("I couldn't understand that. Could you repeat?")
        except sr.RequestError:
            stop_blue_fade()
            set_status("standby")
            speak_text("There was a problem with the speech service.")
        except Exception as e:
            stop_blue_fade()
            set_status("standby")
            print(f"Unexpected error: {e}")
            speak_text("An unexpected error occurred.")
    recognizer = sr.Recognizer()


# --- Wake word listener ---
def wake_word_listener():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Listening for wake word: '{WAKE_WORD}'...")
        r.adjust_for_ambient_noise(source)
        start_blue_fade()

        while True:
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio).lower()
                print(f"Heard: '{text}'")

                if WAKE_WORD in text:
                    print("Wake word detected!")
                    stop_blue_fade()
                    play_audio_file(random.choice(SOUNDS))

                    while True:
                        result = command_processor()
                        if result == "END_CONVERSATION":
                            break

                    print("Returning to wake word mode...")
                    start_blue_fade()

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Speech service error: {e}")
            except KeyboardInterrupt:
                print("Exiting...")
                break