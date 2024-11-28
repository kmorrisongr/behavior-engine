from dataclasses import dataclass
from typing import Callable, Protocol
from uuid import UUID

from behavior_engine.model.base.actor import Actor
from behavior_engine.model.base.entity import Entity
from behavior_engine.simulation.state import WorldState
from behavior_engine.types import SupportsRichComparison


class Interaction(Protocol):
    def __call__(
        self,
        actor_name: UUID,
        entity_name: UUID,
        state: WorldState,
    ) -> None:
        raise NotImplementedError


class SelfInteraction(Protocol):
    def __call__(
        self,
        actor_name: UUID,
        state: WorldState,
    ) -> None:
        raise NotImplementedError


class MovementFunction(Protocol):
    def __call__(
        self,
        actor_name: UUID,
        nearby_perceived_entities: list[Entity],
        state: WorldState,
    ) -> None: ...


def noop(*args: Entity, **kwargs: Entity) -> None:
    pass


@dataclass
class NearestPredicates[T: Entity]:
    filter_pred: Callable[[T], Callable[[T], bool] | None] = noop
    sorted_pred: Callable[[T], Callable[[T], SupportsRichComparison] | None] = noop


class ChoreInteractions(dict[type[Entity], list[Interaction]]):
    """
    A collection of interactions that occur during the chore phase.

    These interactions are run when a given entity type is within physical contact range.
    """


class ChoreInteractionsNot(dict[type[Entity], list[SelfInteraction]]):
    """
    A collection of interactions that occur during the chore phase.

    These interactions are run when a given entity type is _not_ within physical contact range.
    """


class ActionInteractions(dict[type[Entity], list[Interaction]]):
    """
    A collection of interactions that occur during the action phase.

    These interactions are run when a given entity type is within physical contact range.
    """


class MovementPredicates[T: Actor](dict[type[Entity], NearestPredicates[T]]):
    """
    A collection of predicates used during entity querying before the movement phase.

    These predicates control what entities are kept in or prioritized when retrieving the nearest
    entity of a given type.
    """


class BehaviorBlueprint[T: Actor](Protocol):
    chore_interactions: ChoreInteractions
    chore_interactions_not: ChoreInteractionsNot
    action_interactions: ActionInteractions
    movement_predicates: MovementPredicates[T]
    movement: MovementFunction
