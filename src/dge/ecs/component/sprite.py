from .component import Component
import pyglet


class SpriteRenderer(Component):
    def __init__(self, sprite: pyglet.sprite.Sprite, **kwargs):
        super().__init__(**kwargs)
        self.sprite = sprite

    def update(self, x=None, y=None):
        if x is not None:
            self.sprite.x = x
        if y is not None:
            self.sprite.y = y
