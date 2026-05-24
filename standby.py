import os
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

from gpiozero import PWMLED
import time
import sys
from config import BLUE_LED

blue_led = PWMLED(BLUE_LED)

print("Standby mode - breathing blue LED. Press Ctrl+C to exit.")

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