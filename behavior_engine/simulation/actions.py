from uuid import UUID

from behavior_engine.model.base.behavior import Interaction
from behavior_engine.model.base.entity import Entity
from behavior_engine.simulation.state import WorldState


def perform_actions(
    actor_name: UUID,
    behaviors: dict[type[Entity], list[Interaction]],
    nearby_entities: list[Entity],
    state: WorldState,
) -> None:
    for entity in nearby_entities:
        kind = type(entity)
        if kind not in behaviors:
            continue
        for callback in behaviors[kind]:
            callback(actor_name, entity.name, state)
