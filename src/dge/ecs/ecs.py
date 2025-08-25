from .system import SystemManager, System
from .entity import EntityManager, Entity, Signature
from .component import ComponentManager, ComponentType
from .utils.constants import MAX_COMPONENTS
from collections import deque

# https://austinmorlan.com/posts/entity_component_system/


class ECS:
    def __init__(self):
        self.system_manager: SystemManager = SystemManager()
        self.entity_manager: EntityManager = EntityManager()
        self.component_manager: ComponentManager = ComponentManager()
        self.destroy_buffer: deque = deque()

    def _update_signature(self, entity: Entity, component: object, on: bool = True):
        signature = self.entity_manager.get_signature(entity)
        component_type = self.component_manager.get_component_type(type(component))
        signature[int(component_type)] = on
        self.entity_manager.set_signature(entity, signature)

    def create_entity(self):
        return self.entity_manager.create_entity()

    def destroy_entity(self, entity: Entity):
        if entity not in self.destroy_buffer:
            self.destroy_buffer.append(entity)

    def flush_destroy_buffer(self):
        while len(self.destroy_buffer) > 0:
            self._destroy_entity(self.destroy_buffer.popleft())

    def _destroy_entity(self, entity: Entity):
        self.entity_manager.destroy_entity(entity)
        self.component_manager.entity_destroyed(entity)

    def register_component(self, component: type):
        self.component_manager.register_component(component)

    def add_component(self, entity: Entity, component: object):
        self.component_manager.add_component(entity, component)
        self._update_signature(entity, component)

    def remove_component(self, entity: Entity, component: type):
        self.component_manager.remove_component(entity, component)
        self._update_signature(entity, component, on=False)

    def get_component(self, entity: Entity, component: type) -> object:
        return self.component_manager.get_component_array(component).get_data(entity)

    def get_component_type(self, component: type) -> ComponentType:
        return self.component_manager.get_component_type(component)

    def register_system(self, system: type) -> System:
        return self.system_manager.register_system(system)

    def get_query_bundle(self, entity, *components):
        comps = []
        for component in components:
            comps.append(self.get_component(entity, component))
        return entity, tuple(comps)

    def query(self, *components: type):

        signature = Signature(MAX_COMPONENTS)
        for component in components:
            comp_type = self.get_component_type(component)
            signature[comp_type] = True

        return [
            self.get_query_bundle(e, *components)
            for e in self.entity_manager.query(signature)
        ]
