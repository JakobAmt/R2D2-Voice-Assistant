import os
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

from gpiozero import PWMLED
import threading
import time
from config import BLUE_LED, RED_LED

# --- Setup ---
blue_led = PWMLED(BLUE_LED)
red_led = PWMLED(RED_LED)

# --- State ---
blue_fade_active = False
blue_fade_thread = None

# --- Blue LED ---
def blue_led_fade():
    global blue_fade_active
    while blue_fade_active:
        for duty in range(0, 101):
            blue_led.value = duty / 100
            time.sleep(0.02)
            if not blue_fade_active:
                break
        for duty in range(100, -1, -1):
            blue_led.value = duty / 100
            time.sleep(0.02)
            if not blue_fade_active:
                break
    blue_led.value = 0

def start_blue_fade():
    global blue_fade_active, blue_fade_thread
    if not blue_fade_active:
        blue_fade_active = True
        blue_fade_thread = threading.Thread(target=blue_led_fade, daemon=True)
        blue_fade_thread.start()

def stop_blue_fade():
    global blue_fade_active
    blue_fade_active = False
    time.sleep(0.1)
    blue_led.value = 0

# --- Red LED ---
def red_led_on():
    red_led.value = 1

def red_led_off():
    red_led.value = 0

# --- Cleanup ---
def cleanup():
    global blue_fade_active
    blue_fade_active = False
    blue_led.close()
    red_led.close()