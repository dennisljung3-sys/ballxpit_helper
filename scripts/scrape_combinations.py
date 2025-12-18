import requests
from bs4 import BeautifulSoup
import json

URL = "https://ballpit.fandom.com/wiki/Balls"
OUTPUT_FILE = "evolved_combinations.json"

html = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
).text

soup = BeautifulSoup(html, "html.parser")

evolved_combinations = {}

# Gå igenom ALLA tabeller
for table in soup.find_all("table"):
    tbody = table.find("tbody")
    if not tbody:
        continue

    for row in tbody.find_all("tr"):
        cells = row.find_all("td")

        # Vi behöver minst 4 kolumner
        if len(cells) < 4:
            continue

        ball_name = cells[1].get_text(strip=True)
        combo_cell = cells[3]

        if not ball_name:
            continue

        combos = []

        for text in combo_cell.stripped_strings:
            if "+" in text:
                parts = [p.strip() for p in text.split("+")]
                combos.append(parts)

        if combos:
            evolved_combinations[ball_name] = combos

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(evolved_combinations, f, indent=2, ensure_ascii=False)

print(f"Sparade {len(evolved_combinations)} evolved balls.")
