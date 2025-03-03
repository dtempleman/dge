from ..component import Component


class Entity:
    def __init__(self, id):
        self.id = id
        self.components = []

    def add_component(self, component):
        raise NotImplementedError()

    def remove_component(self, component):
        raise NotImplementedError()
