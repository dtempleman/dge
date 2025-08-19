from typing import List
from ecs import Entity, EntitySystem, component
from abc import ABC, abstractmethod


@component
class GenericTriggerComponent:
    # check all entities that have this component
    cause_component_type: type
    active: bool = True
    resetting: bool = False
    triggered: bool = False
    fired: bool = False


class TriggerSystem(EntitySystem):
    def __init__(self, entities):
        super().__init__(entities)

    def update(self):
        for entity in self.entities.get_by_component_types(GenericTriggerComponent):
            if not hasattr(entity, "trigger") or not callable(
                getattr(entity, "trigger")
            ):
                continue
            for trigger in entity.get_components_by_type(GenericTriggerComponent):
                for other in self.entities.get_by_component_types(
                    trigger.cause_component_type
                ):
                    events, ec_map = entity.trigger(trigger, other)
                    self.entities.add(*events)
                    for ent, comps in ec_map.items():
                        self.entities.add_component_to(ent, comps)

                    if not trigger.resetting:
                        self.entities.remove_component_from(entity, trigger)
