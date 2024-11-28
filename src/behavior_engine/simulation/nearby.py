from typing import Callable
from uuid import UUID

from behavior_engine.behavior.blueprint import BehaviorBlueprint
from behavior_engine.model.actor import Actor
from behavior_engine.model.entity import Entity
from behavior_engine.smath.distance import distance, nearby
from behavior_engine.types import Coordinates, SupportsRichComparison


def true_predicate(_: Entity) -> bool:
    return True


def find_nearest_entity[
    T: Entity
](
    position: Coordinates,
    entities: list[T],
    filter_pred: Callable[[T], bool] | None = None,
    sorted_pred: Callable[[T], SupportsRichComparison] | None = None,
) -> (T | None):
    if not entities:
        return None

    if filter_pred is None:
        filter_pred = true_predicate
    filtered_entities = list(filter(filter_pred, entities))

    sorted_entities = filtered_entities
    if sorted_pred is not None:
        sorted_entities = sorted(entities, key=sorted_pred)

    distances = [distance(position, entity.position) for entity in sorted_entities]
    min_distance = min(distances, default=None)
    if min_distance is None:
        return None
    min_indices = [i for i, d in enumerate(distances) if d == min_distance]
    return sorted_entities[min_indices[0]]


def get_nearby_entities(
    position: Coordinates,
    entities: dict[type[Entity], dict[UUID, Entity]],
    within: float,
) -> list[Entity]:
    """
    Get all entities within a certain distance of a position.

    Args:
        position: The position to check from.
        entities: A dictionary of entities, keyed by type.
        within: How far away from the nearest entity to consider "nearby". Will be added to the
            body radius of the nearest entity.

    Returns:
        A list of entities that are nearby, with no more than one for each type.
    """
    nearby_entities = []
    for subentities in entities.values():
        nearest = find_nearest_entity(position, list(subentities.values()))
        if nearest is not None and nearby(position, nearest.position, nearest.body_radius + within):
            nearby_entities.append(nearest)
    return nearby_entities


def get_nearby_perceived_entities[
    T: Actor
](
    actor: T,
    entities: dict[type[Entity], dict[UUID, Entity]],
    behavior_blueprints: dict[type[T], BehaviorBlueprint[T]],
) -> list[Entity]:
    nearby_perceived_entities = []
    for kind, subentities in entities.items():
        filter_pred = (
            behavior_blueprints[type(actor)].movement_predicates[kind].filter_pred(actor)
            if kind in behavior_blueprints[type(actor)].movement_predicates
            else None
        )
        sorted_pred = (
            behavior_blueprints[type(actor)].movement_predicates[kind].sorted_pred(actor)
            if kind in behavior_blueprints[type(actor)].movement_predicates
            else None
        )
        nearest = find_nearest_entity(
            actor.position,
            list(subentities.values()),
            filter_pred=filter_pred,  # type: ignore[arg-type]
            sorted_pred=sorted_pred,  # type: ignore[arg-type]
        )
        if nearest is not None and nearby(
            actor.position, nearest.position, nearest.body_radius + actor.perception_range
        ):
            nearby_perceived_entities.append(nearest)
    return nearby_perceived_entities
