from dge import ecs
import time


class Engine:
    def __init__(self):
        self.running = False
        self.init_entities()

    def update(self, delta):
        for system in ecs.system_manager.systems.values():
            system.update(delta)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def pause(self):
        self.running = False

    def win_con(self):
        return True

    def run(self):
        delta = 0.0
        while self.running:
            start = time.time()
            self.update(delta)
            end = time.time()
            delta = end - start
            if self.win_con():
                self.stop()

    def init_entities(self):
        pass
