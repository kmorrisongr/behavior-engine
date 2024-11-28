from typing import Protocol
from uuid import UUID

from behavior_engine.model.actor import Actor
from behavior_engine.simulation.state import WorldState


class Interaction[T: Actor](Protocol):
    def __call__(
        self,
        actor_name: UUID,
        entity_name: UUID,
        state: WorldState,
    ) -> None:
        raise NotImplementedError


class SelfInteraction[T: Actor](Protocol):
    def __call__(
        self,
        actor_name: UUID,
        state: WorldState,
    ) -> None:
        raise NotImplementedError
