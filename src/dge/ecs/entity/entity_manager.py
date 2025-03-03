from dge.ecs.entity import Entity


class EntityManager:
    def __init__(self):
        self.entities = {}
        self.next_entity_id = 0

    def add_entity(self):
        entity_id = self._new_entity_id()
        entity = Entity(entity_id)
        self.entities[entity_id] = entity
        return entity_id

    def remove_entity(self, entity_id):
        del self.entities[entity_id]

    def get_entity(self, entity_id):
        return self.entities[entity_id]

    def _new_entity_id(self):
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        return entity_id
