from bitarray import bitarray
from typing import List
import numpy as np
from collections import deque

from .utils.constants import MAX_COMPONENTS, MAX_ENTITIES

Entity = np.uint32

MAX_ENTITIES: Entity = Entity(MAX_ENTITIES)

Signature = bitarray


class EntityManager:
    def __init__(self):
        self.living_entity_count: int = 0

        signature = Signature(MAX_COMPONENTS)
        signature.setall(0)
        self.signature_entity_map: List[Signature] = [signature] * MAX_ENTITIES

        self.available_entity_ids: deque = deque()
        self.available_entity_ids.extend([Entity(i) for i in range(0, MAX_ENTITIES)])

    def _validate_entity(self, entity: Entity) -> bool:
        if entity > MAX_ENTITIES:
            raise ValueError

    def create_entity(self) -> Entity:
        if self.living_entity_count < MAX_ENTITIES:
            eid: Entity = self.available_entity_ids.popleft()
            self.living_entity_count += 1
            return eid
        raise ValueError

    def destroy_entity(self, entity: Entity) -> None:
        self._validate_entity(entity)
        self.signature_entity_map[entity].setall(0)
        self.available_entity_ids.append(entity)
        self.living_entity_count -= 1

    def get_signature(self, entity: Entity) -> Signature:
        self._validate_entity(entity)
        return self.signature_entity_map[entity]

    def set_signature(self, entity, signature: Signature) -> None:
        self._validate_entity(entity)
        self.signature_entity_map[entity] = signature
