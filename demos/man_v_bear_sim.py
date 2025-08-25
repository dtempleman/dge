from dge import ecs, Engine, register_component, register_system, logger
from dge.ecs import System
from dge.systems.components import Sprite, Transform, RigidBody

from dataclasses import dataclass
import random
import numpy as np
import time


@register_component()
@dataclass
class Health:
    hp: int
    max_hp: int


@register_component()
@dataclass
class Weapon:
    damage_max: int
    damage_min: int


@register_component()
@dataclass
class Name:
    name: str


@register_system()
class CombatSystem(System):

    def update(self, delta: float):
        for attacker, (wep, a_name, a_trans) in ecs.query(Weapon, Name, Transform):
            for defender, (health, d_name, d_trans) in ecs.query(
                Health, Name, Transform
            ):
                if attacker == defender:
                    continue
                if not (a_trans.position == d_trans.position).all():
                    continue
                damage = random.randint(wep.damage_min, wep.damage_max)
                health.hp -= damage
                logger.log(
                    f"{a_name.name}({attacker}) has dealt {damage} to {d_name.name}({defender}) | {health.hp}/{health.max_hp}"
                )


@register_system()
class DeathSystem(System):

    def update(self, delta: float):
        for entity, (health, name) in ecs.query(Health, Name):
            if health.hp <= 0:
                ecs.destroy_entity(entity)
                name = name.name if name else entity
                logger.log(f"{entity} | {name} has died")


@register_system()
class RandomMoveSystem(System):

    def update(self, delta: float):
        for entity, (rigid_body, transform) in ecs.query(RigidBody, Transform):
            rigid_body.velocity = np.array(
                [
                    random.randint(-1, 1),
                    random.randint(-1, 1),
                    0,
                ]
            )

            for a in range(len(transform.position)):
                if transform.position[a] > 5:
                    rigid_body.velocity[a] = -1
                elif transform.position[a] < 1:
                    rigid_body.velocity[a] = 1


class Game(Engine):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()

    def init_entities(self):
        man = ecs.create_entity()
        ecs.add_component(man, Health(hp=10, max_hp=10))
        ecs.add_component(man, Weapon(damage_max=7, damage_min=4))
        ecs.add_component(man, Name(name="a man"))
        ecs.add_component(man, Sprite(val="m"))
        ecs.add_component(man, Transform())
        ecs.add_component(man, RigidBody(velocity=np.array([0, 0, 0])))

        bear = ecs.create_entity()
        ecs.add_component(bear, Health(hp=20, max_hp=20))
        ecs.add_component(bear, Weapon(damage_max=6, damage_min=0))
        ecs.add_component(bear, Name(name="a bear"))
        ecs.add_component(bear, Sprite(val="B"))
        ecs.add_component(bear, Transform())
        ecs.add_component(bear, RigidBody(velocity=np.array([0, 0, 0])))

    def win_con(self):
        return time.time() - self.start_time > 60


def main():
    ge = Game()
    ge.start()
    ge.run()


if __name__ == "__main__":
    main()
