from dge import ecs, renderer, register_system, System
from .components import Transform, Sprite


@register_system()
class SpriteRenderSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, delta: float):

        for _, (transform, sprite) in ecs.query(Transform, Sprite):
            renderer.render(sprite.val, transform.position)
