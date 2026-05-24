import os
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

from gpiozero import PWMLED
import time
import sys
import random
import threading
import pygame
from config import BLUE_LED, SOUNDS

blue_led = PWMLED(BLUE_LED)

def play_random_sound():
    """Play a random R2D2 sound."""
    sound = random.choice(SOUNDS)
    print(f"Playing: {sound}")
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"Audio error: {e}")
    finally:
        pygame.mixer.quit()

def sound_scheduler():
    """Play a sound every 10 minutes."""
    while True:
        time.sleep(600)
        play_random_sound()

# Start sound scheduler in background
scheduler_thread = threading.Thread(target=sound_scheduler, daemon=True)
scheduler_thread.start()

print("Standby mode - press Ctrl+C to exit.")

try:
    while True:
        for duty in range(0, 101):
            blue_led.value = duty / 100
            time.sleep(0.02)
        for duty in range(100, -1, -1):
            blue_led.value = duty / 100
            time.sleep(0.02)

except KeyboardInterrupt:
    print("\nExiting standby.")
finally:
    blue_led.value = 0
    blue_led.close()
    sys.exit(0)