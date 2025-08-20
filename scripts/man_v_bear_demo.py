from src.dge import ecs
from src.dge.ecs import System, Signature, MAX_COMPONENTS
from dataclasses import dataclass
import random
import time


@dataclass
class Health:
    hp: int = 0
    max_hp: int = 0


@dataclass
class Weapon:
    damage_max: int = 0
    damage_min: int = 0


@dataclass
class Name:
    name: str = ""


class CombatSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, delta: float):
        global ecs

        for attacker in self.entities:
            wep = ecs.get_component(attacker, Weapon)
            a_name = ecs.get_component(attacker, Name)

            for defender in self.entities:
                if attacker == defender:
                    continue
                health = ecs.get_component(defender, Health)
                d_name = ecs.get_component(defender, Name)

                damage = random.randint(wep.damage_min, wep.damage_max)

                health.hp -= damage
                print(
                    f"{a_name.name} has dealt {damage} to {d_name.name} | {health.hp}/{health.max_hp}"
                )


class DeathSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, delta: float):
        global ecs

        for entity in list(self.entities):
            health = ecs.get_component(entity, Health)
            name = ecs.get_component(entity, Name)
            if health.hp <= 0:
                ecs.destroy_entity(entity)
                name = name.name if name else entity
                print(f"{name} has died")


def create_signature(*components: type):
    global ecs
    signature = Signature(MAX_COMPONENTS)
    signature.setall(0)
    for component in components:
        comp_type = ecs.get_component_type(component)
        signature[comp_type] = True
    return signature


def main():
    global ecs

    ecs.register_component(Health)
    ecs.register_component(Weapon)
    ecs.register_component(Name)

    combat = CombatSystem()
    ecs.register_system(combat)
    signature = create_signature(Weapon, Health)
    ecs.set_system_signature(CombatSystem, signature)

    death = DeathSystem()
    ecs.register_system(death)
    signature = create_signature(Health, Name)
    ecs.set_system_signature(DeathSystem, signature)

    man = ecs.create_entity()
    ecs.add_component(man, Health(hp=10, max_hp=10))
    ecs.add_component(man, Weapon(damage_max=7, damage_min=3))
    ecs.add_component(man, Name(name="a man"))

    bear = ecs.create_entity()
    ecs.add_component(bear, Health(hp=20, max_hp=20))
    ecs.add_component(bear, Weapon(damage_max=10, damage_min=0))
    ecs.add_component(bear, Name(name="a bear"))

    delta = 0.0
    while ecs.entity_manager.living_entity_count > 1:
        start = time.time()

        combat.update(delta)
        death.update(delta)

        end = time.time()
        delta = end - start


if __name__ == "__main__":
    main()
