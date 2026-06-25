import time
import board
import busio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# --- Setup OLED ---
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# --- Clear display ---
oled.fill(0)
oled.show()

print("OLED clock running - press Ctrl+C to exit.")

try:
    while True:
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p")
        date_str = now.strftime("%A")
        date_str2 = now.strftime("%B %d, %Y")

        # Create blank image
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        # Load fonts
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Draw time
        draw.text((5, 5), time_str, font=font_large, fill=255)

        # Draw divider line
        draw.line((0, 30, 128, 30), fill=255, width=1)

        # Draw date
        draw.text((5, 35), date_str, font=font_small, fill=255)
        draw.text((5, 50), date_str2, font=font_small, fill=255)

        # Display
        oled.image(image)
        oled.show()

        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting.")
finally:
    oled.fill(0)
    oled.show()