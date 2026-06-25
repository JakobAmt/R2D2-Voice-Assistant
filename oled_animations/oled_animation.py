import time
import board
import busio
import adafruit_ssd1306
from PIL import Image

# --- Setup OLED ---
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
oled.fill(0)
oled.show()

FRAME_SIZE = 1024
FRAME_DELAY = 0.01      # 100ms per frame
ANIM_DURATION = 10     # seconds per animation

def load_frames(filename):
    frames = []
    with open(filename, 'rb') as f:
        while True:
            data = f.read(FRAME_SIZE)
            if len(data) < FRAME_SIZE:
                break
            frames.append(data)
    print(f"Loaded {len(frames)} frames from {filename}")
    return frames

def play_animation(frames, duration):
    """Play animation in a loop for given duration in seconds."""
    end_time = time.time() + duration
    frame_idx = 0
    while time.time() < end_time:
        image = Image.frombytes('1', (128, 64), bytes(frames[frame_idx]))
        oled.image(image)
        oled.show()
        frame_idx = (frame_idx + 1) % len(frames)
        time.sleep(FRAME_DELAY)

# Load both animations
anim1 = load_frames('anim1.bin')
anim2 = load_frames('anim2.bin')
anim3 = load_frames('anim3.bin')
anim4 = load_frames('anim4.bin')

print("Playing animations - Ctrl+C to stop")

try:
    while True:
        print("Playing animation 1...")
        play_animation(anim1, ANIM_DURATION)
        print("Playing animation 2...")
        play_animation(anim2, ANIM_DURATION)
        print("Playing animation 3...")
        play_animation(anim3, ANIM_DURATION)
        print("Playing animation 4...")
        play_animation(anim4, ANIM_DURATION)

except KeyboardInterrupt:
    print("\nExiting.")
finally:
    oled.fill(0)
    oled.show()