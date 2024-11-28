from typing import Protocol
from uuid import UUID

from behavior_engine.model.actor import Actor
from behavior_engine.simulation.state import WorldState


class Interaction[T: Actor](Protocol):
    actor_cls: type[T]

    def get_actor(self, actor_name: UUID, state: WorldState) -> T:
        return state.get_entity(self.actor_cls, actor_name)

    def __call__(
        self,
        actor_name: UUID,
        entity_name: UUID,
        state: WorldState,
    ) -> None:
        raise NotImplementedError


class SelfInteraction[T: Actor](Protocol):
    actor_cls: type[T]

    def get_actor(self, actor_name: UUID, state: WorldState) -> T:
        return state.get_entity(self.actor_cls, actor_name)

    def __call__(
        self,
        actor_name: UUID,
        state: WorldState,
    ) -> None:
        raise NotImplementedError
