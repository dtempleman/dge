from .system import System

COMPONENT_REGISTRY = {}
SYSTEM_REGISTRY = {}


def register_component(name: str):

    def decorate(cls):
        assert issubclass(cls, object)
        assert name not in COMPONENT_REGISTRY
        COMPONENT_REGISTRY[name] = cls
        return cls

    return decorate


def get_component(name: str):
    return COMPONENT_REGISTRY[name]


def register_system(name: str):

    def decorate(cls):
        assert issubclass(cls, System)
        assert name not in SYSTEM_REGISTRY
        SYSTEM_REGISTRY[name] = cls
        return cls

    return decorate


def get_system(name: str):
    return SYSTEM_REGISTRY[name]
