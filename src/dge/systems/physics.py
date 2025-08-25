from dge import ecs, register_system, System
from .components import Transform, RigidBody


@register_system()
class PhysicsSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, delta: float):
        for entity, (transform, rigid_body) in ecs.query(Transform, RigidBody):
            transform.position += rigid_body.velocity
            rigid_body.velocity = rigid_body.velocity * rigid_body.acceleration
