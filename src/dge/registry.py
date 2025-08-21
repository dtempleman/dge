from . import ecs


def register_component():

    def decorate(cls):
        ecs.register_component(cls)
        return cls

    return decorate


def register_system():

    def decorate(cls):
        ecs.register_system(cls)
        return cls

    return decorate
