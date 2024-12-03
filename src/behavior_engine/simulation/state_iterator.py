import logging
from typing import TypeVar

import structlog

from behavior_engine.behavior.blueprint import BehaviorBlueprint
from behavior_engine.log import QuietType, get_logger
from behavior_engine.model.actor import Actor
from behavior_engine.model.entity import Entity
from behavior_engine.simulation.nearby import (
    get_nearby_entities,
    get_nearby_perceived_entities,
)
from behavior_engine.simulation.state import WorldState

T = TypeVar("T", bound=Actor)


class WorldStateIterator:
    def __init__(
        self, log: logging.Logger | structlog.BoundLogger | None | QuietType = None
    ) -> None:
        self.log = get_logger(log)
        # mypy doesn't like this, because T isn't bound inside WorldStateIterator
        # but it communicates (I think) what I want to about the relationship between keys and
        # values in blueprints
        self.blueprints: dict[type[T], BehaviorBlueprint[T]] = {}  # type: ignore[valid-type]

    def add_behavior[T: Actor](self, actor_type: type[T], behavior: BehaviorBlueprint[T]) -> None:
        self.blueprints[actor_type] = behavior

    def get_behavior[T: Actor](self, actor_type: type[T]) -> BehaviorBlueprint[T]:
        return self.blueprints[actor_type]  # pyright: ignore[reportReturnType]

    def step(self, state: WorldState) -> None:
        """
        Perform the next step in the simulation.

        Args:
            state: The current state of the world.
        """
        actors = [v for subdict in state.itertype(Actor) for v in subdict.values()]
        for actor in actors:
            self.log.debug(actor)

            nearby_entities = get_nearby_entities(
                position=actor.position, entities=state.entities, within=actor.body_radius
            )

            self.perform_chores(actor, nearby_entities, state)
            self.perform_actions(actor, nearby_entities, state)

            nearby_perceived_entities = get_nearby_perceived_entities(
                actor=actor,
                entities=state.entities,
                behavior_blueprints=self.blueprints,
            )
            self.perform_movement(actor, nearby_perceived_entities, state)

    def perform_chores(
        self, actor: Actor, nearby_entities: list[Entity], state: WorldState
    ) -> None:
        actor_behaviors = self.get_behavior(type(actor))

        known_kinds: set[type[Entity]] = set()
        for entity in nearby_entities:
            kind = type(entity)
            known_kinds.add(kind)
            if kind not in actor_behaviors.chore_interactions:
                continue
            for icallback in actor_behaviors.chore_interactions[kind]:
                icallback(actor.name, entity.name, state)
        for kind, interactions in actor_behaviors.chore_interactions_not.items():
            if kind in known_kinds:
                continue
            for sicallback in interactions:
                sicallback(actor.name, state)

    def perform_actions(
        self, actor: Actor, nearby_entities: list[Entity], state: WorldState
    ) -> None:
        actor_behaviors = self.get_behavior(type(actor))

        for entity in nearby_entities:
            kind = type(entity)
            if kind not in actor_behaviors.action_interactions:
                continue
            for callback in actor_behaviors.action_interactions[kind]:
                callback(actor.name, entity.name, state)

    def perform_movement(
        self, actor: Actor, nearby_perceived_entities: list[Entity], state: WorldState
    ) -> None:
        actor_behaviors = self.get_behavior(type(actor))
        actor_behaviors.movement(actor.name, nearby_perceived_entities, state)
