from typing import Dict, List

from dge.ecs.component import ComponentType

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

    @property
    def signature_components(self) -> List[type]:
        return []


class SystemManager:
    def __init__(self):
        self.signatures: Dict[str, Signature] = {}
        self.systems: Dict[str, System] = {}

    def register_system(self, system: type):
        if not issubclass(system, System):
            raise ValueError(
                f"Can only register system {system} as its not a subclasses of 'System'."
            )
        sys_name = system.__name__
        if sys_name in self.systems:
            raise ValueError(f"System: {sys_name} is already registered.")
        s = system()
        self.systems[sys_name] = s
        return self.systems[sys_name]

    def set_signature(self, system: type, signature: Signature):
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
