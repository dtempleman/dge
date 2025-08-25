from bitarray import bitarray
from typing import List
import numpy as np
from collections import deque

from .utils.constants import MAX_COMPONENTS, MAX_ENTITIES

Entity = np.uint32

TOTAL_ENTITIES: Entity = Entity(MAX_ENTITIES)

Signature = bitarray


class EntityManager:
    def __init__(self):
        self.living_entities: List[Entity] = []

        self.signature_entity_map: List[Signature] = [
            Signature(MAX_COMPONENTS) for _ in range(TOTAL_ENTITIES)
        ]

        self.available_entity_ids: deque = deque()
        self.available_entity_ids.extend([Entity(i) for i in range(0, TOTAL_ENTITIES)])

    @property
    def living_entity_count(self):
        return len(self.living_entities)

    def _validate_entity(self, entity: Entity):
        if entity > TOTAL_ENTITIES:
            raise ValueError

    def create_entity(self) -> Entity:
        if self.living_entity_count < TOTAL_ENTITIES:
            eid: Entity = self.available_entity_ids.popleft()
            self.living_entities.append(eid)
            return eid
        raise ValueError

    def destroy_entity(self, entity: Entity) -> None:
        self._validate_entity(entity)
        self.signature_entity_map[entity].setall(0)
        self.available_entity_ids.append(entity)
        self.living_entities.remove(entity)

    def get_signature(self, entity: Entity) -> Signature:
        self._validate_entity(entity)
        return self.signature_entity_map[entity]

    def set_signature(self, entity: Entity, signature: Signature) -> None:
        self._validate_entity(entity)
        self.signature_entity_map[entity] = signature

    def query(self, signature: Signature):
        return [
            Entity(entity)
            for entity in self.living_entities
            if (self.signature_entity_map[entity] & signature) == signature
        ]
