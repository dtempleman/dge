from typing import Callable
from ecs import Entity, EntitySystem, component
from enum import Enum


class AlertScope(Enum):
    GLOBAL = 0
    REGIONAL = 1
    LOCAL = 2


class AlertStack(Entity):
    pass


@component
class Alert:
    scope: AlertScope


@component
class Observer:
    alert_type: type
    func: Callable
    scope: AlertScope


class AlertSystem(EntitySystem):
    def __init__(self, entities):
        super().__init__(entities)

    def start(self):
        global alert_stack
        self.entities.add(AlertStack())

    def update(self):
        for observer in self.entities.get_by_component_types(Observer):
            for alert in self.entities.get_by_component_types(observer.alert_type):
                if alert.scope >= observer.scope:
                    observer.func()
