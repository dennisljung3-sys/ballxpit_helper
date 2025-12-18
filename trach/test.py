import requests
from bs4 import BeautifulSoup

html = requests.get(
    "https://ballpit.fandom.com/wiki/Balls",
    headers={"User-Agent": "Mozilla/5.0"}
).text

soup = BeautifulSoup(html, "html.parser")

for img in soup.find_all("img")[:20]:
    print("ALT:", img.get("alt"))
    print("SRC:", img.get("src"))
    print("DATA-SRC:", img.get("data-src"))
    print("-" * 40)
