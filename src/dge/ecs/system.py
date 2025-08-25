from typing import Dict
from abc import ABC, abstractmethod


class System(ABC):

    @abstractmethod
    def update(self, delta: float):
        pass


class SystemManager:
    def __init__(self):
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
