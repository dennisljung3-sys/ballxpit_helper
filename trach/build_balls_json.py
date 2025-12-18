import os
import json

BASE_DIR = "/home/dennis/python_project/ball_x_pitt/images"

balls = []

for stage in ["stage_1", "stage_2", "stage_3"]:
    stage_dir = os.path.join(BASE_DIR, stage)

    for filename in sorted(os.listdir(stage_dir)):
        if not filename.endswith(".png"):
            continue

        ball_id = filename.replace(".png", "")

        balls.append({
            "id": ball_id,
            "stage": stage,
            "image": f"{stage}/{filename}"
        })

with open("balls.json", "w", encoding="utf-8") as f:
    json.dump(balls, f, indent=2)

print(f"Skapade balls.json med {len(balls)} bollar")
