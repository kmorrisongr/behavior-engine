import itertools as itt
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterator
from uuid import UUID

from behavior_engine.model.entity import Entity


@dataclass
class WorldState:
    entities: dict[type[Entity], dict[UUID, Entity]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict())
    )

    def add_entity(self, entity: Entity) -> None:
        self.entities[type(entity)][entity.name] = entity

    def get_entity[T: Entity](self, entity_type: type[T], entity_name: UUID) -> T:
        return self.entities[entity_type][entity_name]  # type: ignore[return-value]

    def get_first(self, entity_type: type[Entity]) -> Entity | None:
        return next(iter(self.entities[entity_type].values()), None)

    def pop_entity[T: Entity](self, entity_type: type[T], entity_name: UUID) -> T:
        return self.entities[entity_type].pop(entity_name)  # type: ignore[return-value]

    def get_entities[T: Entity](self, entity_type: type[T]) -> dict[UUID, T]:
        return self.entities[entity_type]  # type: ignore[return-value]

    def itertype[T: Entity](self, query_type: type[T]) -> Iterator[dict[UUID, T]]:
        """
        Get an iterator over all entities of a given type.

        Args:
            query_type: The type of entity to iterate over. This can be a super type of the key
                types in the entities dictionary, e.g. `Drone`, or even `Entity`.
        """
        for entity_type, entities in self.entities.items():
            if issubclass(entity_type, query_type):
                yield entities  # type: ignore[misc]

    def iter_entities(self) -> Iterator[Entity]:
        """
        Iterate over all entities in the state.

        Yields:
            The next entity in the state, one at a time.
        """
        yield from itt.chain.from_iterable(
            subentities.values() for subentities in self.entities.values()
        )
