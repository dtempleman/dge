import sys
from typing import Dict

from numpy import isin
from .entity import Entity, Signature


class System:
    def __init__(self):
        # todo: im not sure if i like having to update the list of valid entities...
        #       it would probably be better to have a query system that will return
        #       all entities with the given Components, that might involve alot of
        #       refactoring though...
        self.entities: set[Entity] = set([])

    def update(self, delta: float):
        pass


class SystemManager:
    def __init__(self):
        self.signatures: Dict[str, Signature] = {}
        self.systems: Dict[str, type] = {}

    def register_system(self, system: type):
        if not isinstance(system, type):
            system = type(system)
        sys_name = system.__name__
        if sys_name in self.systems:
            raise ValueError(f"System: {sys_name} is already registered.")
        self.systems[sys_name] = system

    def set_signature(self, system: type, signature: Signature):
        if not isinstance(system, type):
            system = type(system)
        sys_name = system.__name__
        if sys_name not in self.systems:
            raise ValueError(f"System {sys_name} is not registered.")
        self.signatures[sys_name] = signature

    def entity_destroyed(self, entity: Entity):
        for system in self.systems.values():
            system.entities.remove(entity)

    def entity_signature_changed(self, entity: Entity, signature: Signature):
        for name, system in self.systems.items():
            sys_sig = self.signatures[name]
            if (sys_sig & signature) == sys_sig:
                system.entities.add(entity)
            else:
                system.entities.discard(entity)
