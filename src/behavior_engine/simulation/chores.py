from uuid import UUID

from behavior_engine.behavior.blueprint import ChoreInteractions, ChoreInteractionsNot
from behavior_engine.model.actor import Actor
from behavior_engine.model.entity import Entity
from behavior_engine.simulation.state import WorldState


def perform_chores[
    T: Actor
](
    actor_name: UUID,
    behaviors: ChoreInteractions[T],
    behaviors_not: ChoreInteractionsNot[T],
    nearby_entities: list[Entity],
    state: WorldState,
) -> None:
    known_kinds = set()
    for entity in nearby_entities:
        kind = type(entity)
        known_kinds.add(kind)
        if kind not in behaviors:
            continue
        for icallback in behaviors[kind]:
            icallback(actor_name, entity.name, state)
    for kind, interactions in behaviors_not.items():
        if kind in known_kinds:
            continue
        for sicallback in interactions:
            sicallback(actor_name, state)
