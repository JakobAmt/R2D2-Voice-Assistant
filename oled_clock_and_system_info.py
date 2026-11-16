import time
import subprocess
import board
import busio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import psutil

# --- Setup OLED ---
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
oled.fill(0)
oled.show()

# --- Settings ---
SCREEN_DURATION = 10   # seconds per screen
REFRESH_RATE = 1       # redraw every second

# --- Fonts (loaded once) ---
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_tiny  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
except OSError:
    font_large = font_small = font_tiny = ImageFont.load_default()

# --- System info helpers ---
def get_cpu_temp():
    try:
        result = subprocess.run(["vcgencmd", "measure_temp"],
                                capture_output=True, text=True)
        return float(result.stdout.replace("temp=", "").replace("'C\n", ""))
    except Exception:
        return None

def get_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            seconds = int(float(f.readline().split()[0]))
        days, rem = divmod(seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes = rem // 60
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        return f"{hours}h {minutes}m"
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
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    draw.text((5, 2), "SYSTEM INFO:", font=font_small, fill=255)
    draw.line((0, 18, 128, 18), fill=255, width=1)
    draw.text((5, 21), f"Temp:   {temp_str}", font=font_tiny, fill=255)
    draw.text((5, 33), f"Uptime: {get_uptime()}", font=font_tiny, fill=255)
    draw.text((5, 45), f"CPU {cpu:.0f}%  RAM {mem:.0f}%", font=font_tiny, fill=255)
    return image

SCREENS = [draw_clock, draw_system_info]

# --- Main loop ---
print("OLED display running - press Ctrl+C to exit.")

try:
    current = 0
    screen_start = time.time()

    while True:
        if time.time() - screen_start >= SCREEN_DURATION:
            current = (current + 1) % len(SCREENS)
            screen_start = time.time()

        oled.image(SCREENS[current]())
        oled.show()
        time.sleep(REFRESH_RATE)

except KeyboardInterrupt:
    print("\nExiting.")
finally:
    oled.fill(0)
    oled.show()