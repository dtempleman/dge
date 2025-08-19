from .entity import Entity
from typing import List, Dict
import numpy as np

ComponentType = np.uint32


class ComponentArray:
    def __init__(self):
        self.components: List[object] = []
        self.entity_to_index: Dict[Entity, int] = {}
        self.index_to_entity: Dict[int, Entity] = {}
        self.size: int = 0

    def insert_data(self, entity: Entity, component: object) -> None:
        if entity not in self.entity_to_index:
            new_index = self.size
            self.entity_to_index[entity] = new_index
            self.index_to_entity[new_index] = entity
            if len(self.components) == new_index:
                self.components.append(component)
            elif len(self.components) < new_index:
                raise ValueError(
                    f"Cannot add a component: index {new_index} is out of range."
                )
            else:
                self.components[new_index] = component
            self.size += 1

    def remove_data(self, entity: Entity) -> None:
        if entity in self.entity_to_index:
            removed_index = self.entity_to_index[entity]
            last_index = self.size - 1
            self.components[removed_index] = self.components[last_index]
            last_entity = self.index_to_entity[last_index]
            self.entity_to_index[last_entity] = removed_index
            self.index_to_entity[removed_index] = last_entity

            del self.entity_to_index[entity]
            del self.index_to_entity[last_index]
            self.size -= 1

    def get_data(self, entity: Entity) -> object | None:
        if entity in self.entity_to_index:
            return self.components[self.entity_to_index[entity]]

    def entity_destroyed(self, entity: Entity) -> None:
        self.remove_data(entity)


class ComponentManager:
    def __init__(self):
        self.str_to_type: Dict[str, ComponentType] = {}
        self.type_to_array: Dict[ComponentType, ComponentArray] = {}
        self.next_component_type: ComponentType = ComponentType(0)

    def register_component(self, component: type):
        if not isinstance(component, type):
            component = type(component)
        comp_name = component.__name__
        if comp_name in self.str_to_type:
            raise ValueError(f"Component: {comp_name} is already registered")

        comp_type = self.next_component_type
        self.str_to_type[comp_name] = comp_type
        self.type_to_array[comp_type] = ComponentArray()
        self.next_component_type += 1

    def get_component_type(self, component: type):
        if not isinstance(component, type):
            component = type(component)
        comp_name = component.__name__
        if comp_name not in self.str_to_type:
            raise ValueError(f"Component: {comp_name} is not registered")
        return self.str_to_type[comp_name]

    def add_component(self, entity: Entity, component: object):
        array = self.get_component_array(component)
        array.insert_data(entity, component)

    def remove_component(self, entity: Entity, component: object):
        array = self.get_component_array(component)
        array.remove_data(entity)

    def entity_destroyed(self, entity: Entity):
        for array in self.type_to_array.values():
            array.entity_destroyed(entity)

    def get_component_array(self, component: type) -> ComponentArray:
        component_type = self.get_component_type(component)
        if component_type in self.type_to_array:
            return self.type_to_array[component_type]
        raise ValueError(
            f"Component type: {component_type} does not have any ComponentArrays"
        )
