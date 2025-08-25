from dge import ecs, renderer
import time


class Engine:
    def __init__(self):
        self.running = False
        self.init_entities()

    def update(self, delta):
        try:
            for system in ecs.system_manager.systems.values():
                system.update(delta)
            renderer.draw()
            time.sleep(1)
        except Exception:
            self.stop()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        renderer.teardown()

    def pause(self):
        self.running = False

    def win_con(self):
        return True

    def run(self):
        delta = 0.0
        while self.running:
            start = time.time()
            self.update(delta)
            ecs.flush_destroy_buffer()
            end = time.time()
            delta = end - start
            if self.win_con():
                self.stop()

    def init_entities(self):
        pass
