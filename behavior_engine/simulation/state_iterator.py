import abc
from typing import TypeVar

from behavior_engine.model.base.actor import Actor
from behavior_engine.model.base.behavior import BehaviorBlueprint
from behavior_engine.simulation.actions import perform_actions
from behavior_engine.simulation.chores import perform_chores
from behavior_engine.simulation.nearby import (
    get_nearby_entities,
    get_nearby_perceived_entities,
)
from behavior_engine.simulation.state import WorldState

T = TypeVar("T", bound=Actor)


class WorldStateIterator(abc.ABC):
    def __init__(self) -> None:
        # mypy doesn't like this, because T isn't bound inside WorldStateIterator
        # but it communicates (I think) what I want to about the relationship between keys and
        # values in blueprints
        self.blueprints: dict[type[T], BehaviorBlueprint[T]] = {}  # type: ignore[valid-type]

    def add_behavior[T: Actor](self, actor_type: type[T], behavior: BehaviorBlueprint[T]) -> None:
        self.blueprints[actor_type] = behavior

    def get_behavior[T: Actor](self, actor_type: type[T]) -> BehaviorBlueprint[T]:
        return self.blueprints[actor_type]

    def iterate_state(self, state: WorldState) -> None:
        actors = [v for subdict in state.itertype(Actor) for v in subdict.values()]
        for actor in actors:
            print(actor)
            actor_behaviors = self.get_behavior(type(actor))

            nearby_entities = get_nearby_entities(actor=actor, entities=state.entities)

            perform_chores(
                actor_name=actor.name,
                behaviors=actor_behaviors.chore_interactions,
                behaviors_not=actor_behaviors.chore_interactions_not,
                nearby_entities=nearby_entities,
                state=state,
            )

            perform_actions(
                actor_name=actor.name,
                behaviors=actor_behaviors.action_interactions,
                nearby_entities=nearby_entities,
                state=state,
            )

            nearby_perceived_entities = get_nearby_perceived_entities(
                actor=actor,
                entities=state.entities,
                behavior_blueprints=self.blueprints,
            )
            actor_behaviors.movement(
                actor_name=actor.name,
                nearby_perceived_entities=nearby_perceived_entities,
                state=state,
            )
