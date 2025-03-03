import pyglet
from dge.ecs.entity import EntityManager
from dge.ecs import component


class GameWindow(pyglet.window.Window):
    def __init__(self, fps=60, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()

    def on_draw(self):
        self.clear()
        self.batch.draw()


class Engine:
    def __init__(
        self,
        height: int = 256,
        width: int = 256,
        title="dge",
        fps=60,
    ):
        self.fps = fps
        self.gravity = -9.8 * self.fps
        pyglet.clock.schedule_interval(self.update, 1 / self.fps)

        self.window = GameWindow(height=height, width=width, caption=title)
        self.world = EntityManager()

        self._build_entities()

    def _build_entities(self):
        entity_id = self.world.add_entity()
        entity = self.world.get_entity(entity_id)
        sprite = pyglet.sprite.Sprite(
            pyglet.image.load("face.png"),
            x=self.window.width // 2 - 16,
            y=self.window.height // 2 - 16,
            batch=self.window.batch,
        )
        entity.add_component(component.SpriteRenderer(parent=entity, sprite=sprite))

    def update(self, dt):
        for entity in self.world.entities.values():
            for compo in entity.components:
                if isinstance(compo, component.SpriteRenderer):
                    y = (compo.sprite.y + (self.gravity * dt)) % self.window.height
                    compo.update(y=y)

    def start(self):
        pyglet.app.run()
