import os
import time
import subprocess
import board
import busio
import psutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# --- Setup OLED ---
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
oled.fill(0)
oled.show()

# --- Settings ---
SCREEN_DURATION = 10     # seconds per screen
TEXT_REFRESH = 1         # redraw clock/system every second
FRAME_DELAY = 0.1        # 100 ms per animation frame
FRAME_SIZE = 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANIM_DIR = os.path.join(BASE_DIR, "oled_animations")
ANIM_FILES = [os.path.join(ANIM_DIR, f"anim{i}.bin") for i in range(1, 6)]

# --- Fonts ---
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_tiny  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
except OSError:
    font_large = font_small = font_tiny = ImageFont.load_default()

# --- System info helpers ---
def get_cpu_temp():
    try:
        result = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True)
        return float(result.stdout.replace("temp=", "").replace("'C\n", ""))
    except Exception:
        return None

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            seconds = int(float(f.readline().split()[0]))
        days, rem = divmod(seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes = rem // 60
        return f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"
    except Exception:
        return "unknown"

# --- Screens ---
def draw_clock():
    now = datetime.now()
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((5, 5), now.strftime("%I:%M:%S %p"), font=font_large, fill=255)
    draw.line((0, 30, 128, 30), fill=255, width=1)
    draw.text((5, 35), now.strftime("%A"), font=font_small, fill=255)
    draw.text((5, 50), now.strftime("%B %d, %Y"), font=font_small, fill=255)
    return image

def draw_system_info():
    temp = get_cpu_temp()
    temp_str = f"{temp:.1f} C" if temp is not None else "N/A"
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((5, 2), "SYSTEM INTEL", font=font_small, fill=255)
    draw.line((0, 18, 128, 18), fill=255, width=1)
    draw.text((5, 21), f"Temp:   {temp_str}", font=font_tiny, fill=255)
    draw.text((5, 33), f"Uptime: {get_uptime()}", font=font_tiny, fill=255)
    draw.text((5, 45), f"CPU {psutil.cpu_percent():.0f}%  RAM {psutil.virtual_memory().percent:.0f}%",
              font=font_tiny, fill=255)
    return image

# --- Animations ---
def load_frames(filename):
    frames = []
    try:
        with open(filename, "rb") as f:
            while True:
                data = f.read(FRAME_SIZE)
                if len(data) < FRAME_SIZE:
                    break
                frames.append(data)
    except FileNotFoundError:
        print(f"WARNING: {filename} not found, skipping.")
        return []
    print(f"Loaded {len(frames)} frames from {os.path.basename(filename)}")
    return frames

def make_animation_renderer(frames):
    """Returns a draw function that steps through the frames, starting from frame 0."""
    state = {"i": 0}
    def render():
        image = Image.frombytes("1", (128, 64), bytes(frames[state["i"]]))
        state["i"] = (state["i"] + 1) % len(frames)
        return image
    return render

animations = [load_frames(p) for p in ANIM_FILES]
animations = [a for a in animations if a]  # skip missing/empty files

# --- Playback ---
def run_screen(render, duration, delay):
    end = time.time() + duration
    while time.time() < end:
        oled.image(render())
        oled.show()
        time.sleep(delay)

# --- Main loop ---
print(f"OLED display running with {len(animations)} animations - press Ctrl+C to exit.")

try:
    while True:
        if animations:
            for frames in animations:
                run_screen(draw_clock, SCREEN_DURATION, TEXT_REFRESH)
                run_screen(draw_system_info, SCREEN_DURATION, TEXT_REFRESH)
                run_screen(make_animation_renderer(frames), SCREEN_DURATION, FRAME_DELAY)
        else:
            # No animation files found, just alternate clock and system info
            run_screen(draw_clock, SCREEN_DURATION, TEXT_REFRESH)
            run_screen(draw_system_info, SCREEN_DURATION, TEXT_REFRESH)

except KeyboardInterrupt:
    print("\nExiting.")
finally:
    oled.fill(0)
    oled.show()