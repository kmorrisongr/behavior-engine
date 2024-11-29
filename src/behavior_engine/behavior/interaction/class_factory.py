from typing import TypeVar
from uuid import UUID

from behavior_engine.behavior.interaction import (
    Interaction,
    InteractionCall,
    InteractionCreator,
    SelfInteraction,
    SelfInteractionCall,
    SelfInteractionCreator,
)
from behavior_engine.model.actor import Actor
from behavior_engine.simulation.state import WorldState

T = TypeVar("T", bound=Actor, covariant=True)


def InteractionFactory(actor_cls: type[T]) -> InteractionCreator[T]:
    """
    Create an Interaction class with a get_actor method.

    The intended use is as a decorator.

    Args:
        actor_cls: The actor class to use for the get_actor method.

    Returns:
        A function that adds a get_actor method to an `InteractionCall` class definition.
    """

    def decorator(call_cls: type[InteractionCall]) -> type[Interaction[T]]:
        def get_actor(cls: type[object], actor_name: UUID, state: WorldState) -> T:
            return state.get_entity(actor_cls, actor_name)

        setattr(call_cls, "get_actor", classmethod(get_actor))
        return call_cls  # pyright: ignore[reportReturnType]

    return decorator


def SelfInteractionFactory(actor_cls: type[T]) -> SelfInteractionCreator[T]:
    """
    Create an SelfInteraction class with a get_actor method.

    The intended use is as a decorator.

    Args:
        actor_cls: The actor class to use for the get_actor method.

    Returns:
        A function that adds a get_actor method to a `SelfInteractionCall` class definition.
    """

    def decorator(call_cls: type[SelfInteractionCall]) -> type[SelfInteraction[T]]:
        def get_actor(cls: type[object], actor_name: UUID, state: WorldState) -> T:
            return state.get_entity(actor_cls, actor_name)

        setattr(call_cls, "get_actor", classmethod(get_actor))
        return call_cls  # pyright: ignore[reportReturnType]

    return decorator
