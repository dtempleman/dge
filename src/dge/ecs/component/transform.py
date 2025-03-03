from .component import Component


class Transform2D(Component):
    def __init__(self, x: float = 0, y: float = 0, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y

    def move_to(self, x: float, y: float):
        self.x = x
        self.y = y
