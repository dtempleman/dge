from dge import ecs, Engine, register_component, register_system
from dge.ecs import System

from dataclasses import dataclass
import random


@register_component()
@dataclass
class Health:
    hp: int = 0
    max_hp: int = 0


@register_component()
@dataclass
class Weapon:
    damage_max: int = 0
    damage_min: int = 0


@register_component()
@dataclass
class Name:
    name: str = ""


@register_system()
class CombatSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, delta: float):

        for attacker in self.entities:
            wep = ecs.get_component(attacker, Weapon)
            a_name = ecs.get_component(attacker, Name)

            for defender in self.entities:
                if attacker == defender:
                    continue
                health = ecs.get_component(defender, Health)
                d_name = ecs.get_component(defender, Name)

                damage = random.randint(
                    getattr(wep, "damage_min"), getattr(wep, "damage_max")
                )
                setattr(health, "hp", getattr(health, "hp") - damage)
                print(
                    f"{getattr(a_name, "name")} has dealt {damage} to {getattr(d_name, "name")} | {getattr(health, "hp")}/{getattr(health, "max_hp")}"
                )

    @property
    def signature_compoenents(self):
        return [Health, Weapon]


@register_system()
class DeathSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, delta: float):

        for entity in list(self.entities):
            health = ecs.get_component(entity, Health)
            name = ecs.get_component(entity, Name)
            if getattr(health, "hp") <= 0:
                ecs.destroy_entity(entity)
                name = getattr(name, "name") if name else entity
                print(f"{name} has died")

    @property
    def signature_compoenents(self):
        return [Health, Name]


class Game(Engine):
    def __init__(self):
        super().__init__()

    def init_entities(self):
        man = ecs.create_entity()
        ecs.add_component(man, Health(hp=10, max_hp=10))
        ecs.add_component(man, Weapon(damage_max=7, damage_min=3))
        ecs.add_component(man, Name(name="a man"))

        bear = ecs.create_entity()
        ecs.add_component(bear, Health(hp=20, max_hp=20))
        ecs.add_component(bear, Weapon(damage_max=10, damage_min=0))
        ecs.add_component(bear, Name(name="a bear"))

    def win_con(self):
        return ecs.entity_manager.living_entity_count < 2


def main():
    ge = Game()
    ge.start()
    ge.run()


if __name__ == "__main__":
    main()
