from .game_loggers import GameLogger

logger = GameLogger()

from .ecs import ECS  # noqa: E402

ecs = ECS()

from .renderer import Renderer  # noqa: E402

renderer = Renderer()

from .ecs import System, SystemManager, Entity, EntityManager  # noqa: F401,E402
from .registry import register_component, register_system  # noqa: F401,E402
from .systems import *  # noqa: F401,F403,E402
from .engine import Engine  # noqa: F401,E402
