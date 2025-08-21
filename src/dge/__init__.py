from .ecs import ECS

ecs = ECS()

from .registry import register_component, register_system  # noqa: F401,E402
from .engine import Engine  # noqa: F401,E402
