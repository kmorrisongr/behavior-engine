from dataclasses import dataclass
from typing import Callable, Protocol

from behavior_engine.behavior.interaction import Interaction, SelfInteraction
from behavior_engine.behavior.movement import MovementFunction
from behavior_engine.model.actor import Actor
from behavior_engine.model.entity import Entity
from behavior_engine.types import SupportsRichComparison


class ChoreInteractions[T: Actor](dict[type[Entity], list[Interaction[T]]]):
    """
    A collection of interactions that occur during the chore phase.

    These interactions are run when a given entity type is within physical contact range.
    """


class ChoreInteractionsNot[T: Actor](dict[type[Entity], list[SelfInteraction[T]]]):
    """
    A collection of interactions that occur during the chore phase.

    These interactions are run when a given entity type is _not_ within physical contact range.
    """


class ActionInteractions[T: Actor](dict[type[Entity], list[Interaction[T]]]):
    """
    A collection of interactions that occur during the action phase.

    These interactions are run when a given entity type is within physical contact range.
    """


def noop(*args: Entity, **kwargs: Entity) -> None:
    pass


@dataclass
class NearestPredicates[T: Entity]:
    filter_pred: Callable[[T], Callable[[T], bool] | None] = noop
    sorted_pred: Callable[[T], Callable[[T], SupportsRichComparison] | None] = noop


class MovementPredicates[T: Actor](dict[type[Entity], NearestPredicates[T]]):
    """
    A collection of predicates used during entity querying before the movement phase.

    These predicates control what entities are kept in or prioritized when retrieving the nearest
    entity of a given type.
    """


class BehaviorBlueprint[T: Actor](Protocol):
    chore_interactions: ChoreInteractions[T]
    chore_interactions_not: ChoreInteractionsNot[T]
    action_interactions: ActionInteractions[T]
    movement_predicates: MovementPredicates[T]
    movement: MovementFunction
