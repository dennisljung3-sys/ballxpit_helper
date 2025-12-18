import json
import re
from pathlib import Path

INPUT_FILE = "evolved_combinations_normalized.json"
OUTPUT_FILE = "evolved_combinations_final.json"


def normalize_name(name: str) -> str:
    """
    Normaliserar ett bollnamn:
    - lowercase
    - ersätter mellanslag med _
    - tar bort specialtecken
    - lägger till _ball om det saknas
    """
    name = name.lower()
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-z0-9_]", "", name)

    if not name.endswith("_ball"):
        name += "_ball"

    return name


def normalize_combinations(data: dict) -> dict:
    """
    Normaliserar:
    - evolved ball-namnet (key)
    - varje boll i varje kombination
    """
    normalized = {}

    for evolved_ball, combos in data.items():
        evolved_ball_norm = normalize_name(evolved_ball)

        normalized_combos = []
        for combo in combos:
            # combo är redan en LISTA, t.ex. ["iron", "ghost"]
            normalized_combo = [normalize_name(ball) for ball in combo]
            normalized_combos.append(normalized_combo)

        normalized[evolved_ball_norm] = normalized_combos

    return normalized


def main():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    normalized_data = normalize_combinations(data)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(normalized_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Normaliserade kombinationer sparade i {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
