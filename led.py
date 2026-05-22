import RPi.GPIO as GPIO
import threading
import time
from config import BLUE_LED, RED_LED

# --- Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

pwm_blue = GPIO.PWM(BLUE_LED, 1000)
pwm_red = GPIO.PWM(RED_LED, 1000)
pwm_blue.start(0)
pwm_red.start(0)

# --- State ---
blue_fade_active = False
blue_fade_thread = None
led_lock = threading.Lock()

# --- Blue LED ---
def blue_led_fade():
    global blue_fade_active
    while blue_fade_active:
        for duty in range(0, 101):
            with led_lock:
                pwm_blue.ChangeDutyCycle(duty)
            time.sleep(0.02)
            if not blue_fade_active:
                break
        for duty in range(100, -1, -1):
            with led_lock:
                pwm_blue.ChangeDutyCycle(duty)
            time.sleep(0.02)
            if not blue_fade_active:
                break
    with led_lock:
        pwm_blue.ChangeDutyCycle(0)

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
    with led_lock:
        pwm_blue.ChangeDutyCycle(0)

# --- Red LED ---
def red_led_on():
    with led_lock:
        pwm_red.ChangeDutyCycle(100)

def red_led_off():
    with led_lock:
        pwm_red.ChangeDutyCycle(0)

# --- Cleanup ---
def cleanup():
    global blue_fade_active
    blue_fade_active = False
    pwm_blue.stop()
    pwm_red.stop()
    GPIO.cleanup()