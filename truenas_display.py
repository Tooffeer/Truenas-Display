import time
import requests
from waveshare_epd import epd2in13_v4
from PIL import Image, ImageDraw, ImageFont

# Api config
API_URL = "https://<ip address here>/api/v2.0" # Truenas IP here
API_KEY = "" # Api key here
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_pool_info():
    info = requests.get(f"{API_URL}/pool", headers=HEADERS, verify=False, timeout=5)
    return info.json()

def main():
    # Initialize and clear display
    epd = epd2in13_v4.EPD()
    epd.init()
    epd.Clear()

    # Draw the screen
    # Create a blank canvas
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    # Fonts (default bitmap — can be swapped for TTF later)
    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    # --- Pool Info ---
    y = 55
    for pool in pools:
        pool_name = pool["name"]
        status = pool["status"]
        draw.text((5, y), f"Pool: {pool_name}", font=font_small, fill=0)
        draw.text((120, y), f"{status}", font=font_small, fill=0)
        y += 15

    # Send to e-ink display
    epd.display(epd.getbuffer(image))