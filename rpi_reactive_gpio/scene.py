import time
from abc import ABC
from pin_manager import PinManagerProtocol, Tickable
from buttons import ButtonClick


class Scene(ABC):
    def main_loop(self, update_interval: float = 1.0, ticks_count: int = 100):
        attributes = [getattr(self, a) for a in dir(self)]
        self.managers = filter(lambda a: isinstance(a, PinManagerProtocol), attributes)
        self.tickables = filter(lambda a: isinstance(a, Tickable), attributes)
        self.events = filter(lambda a: isinstance(a, ButtonClick), attributes)
        
        for event in self.events:
            event.pass_args = [self]
        
        while True:
            self.update_all()
            for i in range(ticks_count):
                self.tick_all(i / ticks_count)
                time.sleep(update_interval / ticks_count)
                
    def update_all(self):
        for manager in self.managers:
            manager.update(self)
            
    def tick_all(self, period: float = 1.0):
        '''period must be in range 0.0...1.0'''
        for tickable in self.tickables:
            tickable.tick(period)
