from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Ball:
    name: str
    stage: int   # 1, 2, 3
    image_path: str


@dataclass(frozen=True)
class Recipe:
    result: str
    ingredients: List[str]
