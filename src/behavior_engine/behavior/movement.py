from typing import Protocol
from uuid import UUID

from behavior_engine.model.entity import Entity
from behavior_engine.simulation.state import WorldState


class MovementFunction(Protocol):
    def __call__(
        self,
        actor_name: UUID,
        nearby_perceived_entities: list[Entity],
        state: WorldState,
    ) -> None: ...
