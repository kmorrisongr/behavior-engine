import math

from behavior_engine.types import Coordinates


def distance(a: Coordinates, b: Coordinates) -> float:
    return round(math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2), 3)


def nearby(a: Coordinates, b: Coordinates, radius: float) -> bool:
    return distance(a, b) <= radius
