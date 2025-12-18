import os
import re

BASE_DIR = "/home/dennis/python_project/ball_x_pitt/images"


def normalize_name(name: str) -> str:
    name = name.lower()
    name = name.replace(" ball", "")
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name


for stage in ["stage_1", "stage_2", "stage_3"]:
    stage_dir = os.path.join(BASE_DIR, stage)

    for filename in os.listdir(stage_dir):
        if not filename.endswith(".png"):
            continue

        old_path = os.path.join(stage_dir, filename)

        base = filename.replace(".png", "")
        new_name = normalize_name(base) + ".png"
        new_path = os.path.join(stage_dir, new_name)

        if old_path != new_path:
            print(f"{filename} → {new_name}")
            os.rename(old_path, new_path)
