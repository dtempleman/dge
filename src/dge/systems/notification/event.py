from typing import List
from ecs import Entity, EntitySystem, component
from abc import ABC, abstractmethod


@component
class TimerComponent:
    # when length == 0, the timer is over
    length: int
    # the period is the amount of 'ticks' to before decrementing length
    period: int = 1


class Event(Entity):
    def __init__(self):
        super().__init__()
        self.live = True
        self.active = True

    def end(self):
        self.live = False

    @abstractmethod
    def update(self):
        pass


class EventSystem(EntitySystem):
    def __init__(self, entities):
        super().__init__(entities)

    def start(self):
        self._load_startup_events()

    def update(self):
        for event in self.entities.get_by_entity_types(Event):
            if event.live:
                event.update()
            else:
                self.entities.delayed_delete(event)

    def _load_startup_events(self):
        pass

    def fire_trigger(self, trigger, event):

        if trigger.is_triggered:
            events = trigger.fire(event)
            self.entities.add(*events)
