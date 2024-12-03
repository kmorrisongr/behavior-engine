from dataclasses import dataclass
from typing import Any, Protocol, Self

Degrees = float


@dataclass
class Coordinates:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def copy(self) -> Self:
        return self.__class__(self.x, self.y)

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


@dataclass
class PolarCoordinates:
    r: float
    theta: Degrees

    def __str__(self) -> str:
        return f"{self.r} @ {self.theta}°"

    def copy(self) -> Self:
        return self.__class__(self.r, self.theta)

    def set_theta(self, theta: Degrees) -> None:
        """
        Assign a new value to theta.

        This method is used to ensure that theta is always between 0 and 360 degrees.
        """
        self.theta = theta % 360


@dataclass
class Velocity(PolarCoordinates):
    """Describe velocity in terms of speed and direction."""


class SupportsLT(Protocol):
    def __lt__(self, other: Any) -> bool: ...


class SupportsGT(Protocol):
    def __gt__(self, other: Any) -> bool: ...


SupportsRichComparison = SupportsLT | SupportsGT
