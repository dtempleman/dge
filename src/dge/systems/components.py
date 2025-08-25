from dge import register_component

from dataclasses import dataclass, field
import numpy as np


@register_component()
@dataclass
class Sprite:
    val: str


@register_component()
@dataclass
class RigidBody:
    velocity: np.ndarray = field(default_factory=lambda: np.array([0, 0, 0]))
    acceleration: np.ndarray = field(default_factory=lambda: np.array([1, 0, 0]))


@register_component()
@dataclass
class Transform:
    position: np.ndarray = field(default_factory=lambda: np.array([0, 0, 0]))
