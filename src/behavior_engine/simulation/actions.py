from uuid import UUID

from behavior_engine.behavior.blueprint import ActionInteractions
from behavior_engine.model.actor import Actor
from behavior_engine.model.entity import Entity
from behavior_engine.simulation.state import WorldState


def perform_actions[
    T: Actor
](
    actor_name: UUID,
    behaviors: ActionInteractions[T],
    nearby_entities: list[Entity],
    state: WorldState,
) -> None:
    for entity in nearby_entities:
        kind = type(entity)
        if kind not in behaviors:
            continue
        for callback in behaviors[kind]:
            callback(actor_name, entity.name, state)
