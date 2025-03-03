from dge.ecs.component import Component


class Entity:
    def __init__(self, id):
        self.id = id
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, component):
        self.components.remove(component)

    def update(self):
        pass
