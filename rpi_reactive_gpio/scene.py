import time
from abc import ABC
from .pin_manager import PinManagerProtocol, Tickable
from .buttons import ButtonClick


class Scene(ABC):
    
    _is_running = False
    
    def main_loop(self, update_interval: float = 1.0, ticks_count: int = 100):
        self._is_running = True
        
        attributes = [getattr(self, a) for a in dir(self)]
        self.managers = filter(lambda a: isinstance(a, PinManagerProtocol), attributes)
        self.tickables = filter(lambda a: isinstance(a, Tickable), attributes)
        self.events = filter(lambda a: isinstance(a, ButtonClick), attributes)
        
        for event in self.events:
            event.pass_args = [self]
        
        while self._is_running:
            self._update_all()
            for i in range(ticks_count):
                self._tick_all(i / ticks_count)
                time.sleep(update_interval / ticks_count)
                
    def stop(self):
        self._is_running = False
                
    def _update_all(self):
        for manager in self.managers:
            manager.update(self)
            
    def _tick_all(self, period: float = 1.0):
        '''period must be in range 0.0...1.0'''
        for tickable in self.tickables:
            tickable.tick(period)
