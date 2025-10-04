import time
import requests
from waveshare_epd import epd2in13_V4
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
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear()

    # Draw the screen
    # Create a blank canvas
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    # Fonts
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)

    # Pool Info
    y = 0
    pools = get_pool_info()
    for pool in pools:
        pool_name = pool["name"]
        status = pool["status"]

        free = int(pool["free"])
        used = int(pool["allocated"])
        
        gb = 1024 ** 3
        free_gb = free / gb
        used_gb = used / gb
        
        

        # Print text
        draw.text((5, y), f"Pool: {pool_name}", font=font_small, fill=0)
        draw.text((120, y), f"{status}", font=font_small, fill=0)

        y += 15
        draw.text((120, y), f"Free: {free_gb}", font=font_small, fill=0)
        y += 15
        draw.text((120, y), f"Used: {used_gb}", font=font_small, fill=0)

        percentage = (used / (free + used)) * 100

        y += 15
        draw.text((120, y), f"{percentage:.1f}%", font=font_small, fill=0)

    # Send to e-ink display
    epd.display(epd.getbuffer(image))
    epd.sleep() # Sleep

if __name__ == "__main__":
    main()