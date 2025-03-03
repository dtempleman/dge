from .entity import Entity


class EntityManager:
    def __init__(self):
        self.entiteis = []

    def add_entity(self, entity):
        raise NotImplementedError()

    def remove_entity(self, entity_id):
        raise NotImplementedError()

    def get_entity(self, entity_id):
        raise NotImplementedError()
