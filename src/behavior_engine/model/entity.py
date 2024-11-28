from dataclasses import dataclass, field
from functools import cached_property
from uuid import UUID, uuid4

from behavior_engine.types import Coordinates, Velocity


@dataclass
class Entity:
    position: Coordinates
    velocity: Velocity
    body_radius: float = 3.0

    @cached_property
    def name(self) -> UUID:
        return uuid4()


@dataclass
class StationaryEntity(Entity):
    velocity: Velocity = field(default_factory=lambda: Velocity(0.0, 0.0))
