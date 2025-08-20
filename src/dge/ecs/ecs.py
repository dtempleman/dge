from .system import SystemManager, System
from .entity import EntityManager, Entity, Signature
from .component import ComponentManager


# https://austinmorlan.com/posts/entity_component_system/


class ECS:
    def __init__(self):
        self.system_manager: SystemManager = SystemManager()
        self.entity_manager: EntityManager = EntityManager()
        self.component_manager: ComponentManager = ComponentManager()

    def _update_signature(self, entity: Entity, component: object, on: bool = True):
        signature = self.entity_manager.get_signature(entity)
        component_type = self.component_manager.get_component_type(type(component))
        signature[int(component_type)] = on
        self.entity_manager.set_signature(entity, signature)
        self.system_manager.entity_signature_changed(entity, signature)

    def create_entity(self):
        return self.entity_manager.create_entity()

    def destroy_entity(self, entity: Entity):
        self.entity_manager.destroy_entity(entity)
        self.component_manager.entity_destroyed(entity)
        self.system_manager.entity_destroyed(entity)

    def register_component(self, component: type):
        self.component_manager.register_component(component)

    def add_component(self, entity: Entity, component: object):
        self.component_manager.add_component(entity, component)
        self._update_signature(entity, component)

    def remove_component(self, entity: Entity, component: object):
        self.component_manager.remove_component(entity, component)
        self._update_signature(entity, component, on=False)

    def get_component(self, entity: Entity, component: type):
        return self.component_manager.get_component_array(component).get_data(entity)

    def get_component_type(self, component: type):
        return self.component_manager.get_component_type(component)

    def register_system(self, system: System):
        self.system_manager.register_system(system)

    def set_system_signature(self, system: System, signature: Signature):
        self.system_manager.set_signature(system, signature)
