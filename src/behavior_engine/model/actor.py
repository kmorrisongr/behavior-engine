from dataclasses import dataclass, field

from behavior_engine.model.entity import Entity
from behavior_engine.types import Degrees, Velocity


@dataclass
class Actor(Entity):
    """
    An entity that interacts with other entities.

    An actor does not have to have any "agency": it can be a static object like a rock. But it can
    have defined behavior that dictates how it interacts with other nearby entities.
    """

    # How wide a view the actor has, centered on its heading
    perception_angle: Degrees = 90.0
    # From edge of actor's body
    perception_range: float = 5.0

    @property
    def full_name(self) -> str:
        return f"{type(self).__name__}|{self.name}"

    def __str__(self) -> str:
        return f"{self.full_name}: {self.position}\tgoing {self.velocity}"


@dataclass
class StationaryActor(Actor):
    velocity: Velocity = field(default_factory=lambda: Velocity(0.0, 0.0))
