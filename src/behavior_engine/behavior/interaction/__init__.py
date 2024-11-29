from typing import Protocol, TypeVar
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
    def get_actor(cls, actor_cls: type[T], state: WorldState) -> T: ...


class SelfInteraction[T: Actor](SelfInteractionCall):
    @classmethod
    def get_actor(cls, actor_cls: type[T], state: WorldState) -> T: ...


class InteractionCreator[T: Actor](Protocol):
    def __call__(self, call_cls: type[InteractionCall]) -> type[Interaction[T]]: ...


class SelfInteractionCreator[T: Actor](Protocol):
    def __call__(self, call_cls: type[SelfInteractionCall]) -> type[SelfInteraction[T]]: ...


T = TypeVar("T", bound=Actor, covariant=True)


def InteractionFactory(actor_cls: type[T]) -> InteractionCreator[T]:
    def decorator(call_cls: type[InteractionCall]) -> type[Interaction[T]]:
        def get_actor(cls: type[object], actor_name: UUID, state: WorldState) -> T:
            return state.get_entity(actor_cls, actor_name)

        setattr(call_cls, "get_actor", classmethod(get_actor))
        return call_cls  # pyright: ignore[reportReturnType]

    return decorator


def SelfInteractionFactory(actor_cls: type[T]) -> SelfInteractionCreator[T]:
    def decorator(call_cls: type[SelfInteractionCall]) -> type[SelfInteraction[T]]:
        def get_actor(cls: type[object], actor_name: UUID, state: WorldState) -> T:
            return state.get_entity(actor_cls, actor_name)

        setattr(call_cls, "get_actor", classmethod(get_actor))
        return call_cls  # pyright: ignore[reportReturnType]

    return decorator
