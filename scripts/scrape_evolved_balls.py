import requests
from bs4 import BeautifulSoup
import os
import time

BASE_URL = "https://ballpit.fandom.com/wiki/Balls"
OUTPUT_DIR = "/home/dennis/python_project/ball_x_pitt/images/stage_2"

os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (BallXPitScraper/1.0)"
}

html = requests.get(BASE_URL, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

count = 0
download = False

START_BALL = "Assassin Ball"
END_BALL = "Nosferatu Ball"

for img in soup.find_all("img"):
    alt = img.get("alt")
    src = img.get("data-src") or img.get("src")

    if not alt or not src:
        continue

    # Endast boll-ikoner
    if not alt.lower().startswith("icon for"):
        continue

    # Extrahera bollnamn
    name = (
        alt.replace("Icon for the ", "")
        .replace("Icon For the ", "")
        .replace("Icon for ", "")
        .replace("Icon For ", "")
        .strip()
    )

    # Start / stopp
    if name == START_BALL:
        download = True

    if not download:
        continue

    # Hoppa över placeholders
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

    if name == END_BALL:
        break

print(f"Klar! {count} Evolved Balls nedladdade.")
