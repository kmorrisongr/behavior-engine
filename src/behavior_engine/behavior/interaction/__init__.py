from typing import Protocol
from uuid import UUID

from behavior_engine.model.actor import Actor
from behavior_engine.simulation.state import WorldState


class InteractionCall(Protocol):
    def __call__(
        self,
        actor_name: UUID,
        entity_name: UUID,
        state: WorldState,
    ) -> None: ...


class SelfInteractionCall(Protocol):
    def __call__(
        self,
        actor_name: UUID,
        state: WorldState,
    ) -> None: ...


class Interaction[T: Actor](InteractionCall):
    @classmethod
    def get_actor(cls, actor_name: UUID, state: WorldState) -> T: ...


class SelfInteraction[T: Actor](SelfInteractionCall):
    @classmethod
    def get_actor(cls, actor_name: UUID, state: WorldState) -> T: ...


class InteractionCreator[T: Actor](Protocol):
    def __call__(self, call_cls: type[InteractionCall]) -> type[Interaction[T]]: ...


class SelfInteractionCreator[T: Actor](Protocol):
    def __call__(self, call_cls: type[SelfInteractionCall]) -> type[SelfInteraction[T]]: ...
