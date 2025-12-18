import requests
from bs4 import BeautifulSoup
import os
import time

BASE_URL = "https://ballpit.fandom.com/wiki/Balls"
OUTPUT_DIR = "/home/dennis/python_project/ball_x_pitt/images/stage_1"

os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (BallXPitScraper/1.0)"
}

html = requests.get(BASE_URL, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

count = 0
download = False

for img in soup.find_all("img"):
    alt = img.get("alt")
    src = img.get("data-src") or img.get("src")

    if not alt or not src:
        continue

    # Vi vill bara ha boll-ikoner
    if not alt.lower().startswith("icon for"):
        continue

    # Plocka ut bollnamnet
    # "Icon for the Bleed Ball" → "Bleed Ball"
    name = (
        alt.replace("Icon for the ", "")
        .replace("Icon For ", "")
        .strip()
    )

    # Start / stopp: Base Balls
    if name == "Bleed Ball":
        download = True

    if not download:
        continue

    # Hoppa över tomma placeholders
    if src.startswith("data:image"):
        continue

    filename = name.replace(" ", "_").lower() + ".png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(filepath):
        continue

    print(f"Laddar ner: {filename}")
    img_data = requests.get(src, headers=headers).content

    with open(filepath, "wb") as f:
        f.write(img_data)

    count += 1
    time.sleep(0.4)

    if name == "Wind Ball":
        break

print(f"Klar! {count} Base Balls nedladdade.")
