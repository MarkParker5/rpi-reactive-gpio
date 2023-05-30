from __future__ import annotations
from typing import Callable, Protocol, runtime_checkable


@runtime_checkable
class Tickable(Protocol):
    def tick(self, period: float = 1.0):
        '''period must be in range 0.0...1.0'''
        pass
    
@runtime_checkable
class PinManagerProtocol(Tickable, Protocol):
    
    def update(self, *args, **kwargs):
        pass
    
    def __call__(self, get_pin_state: Callable) -> PinManagerProtocol:
        '''decorator for setting get_pin_state function that updates led state'''
        pass

tickables: list[Tickable] = []
managers: list[PinManagerProtocol] = []
    
def tick_all_managers(period: float = 1.0):
    '''period must be in range 0.0...1.0'''
    for tickable in tickables:
        tickable.tick(period)
    
def update_all_managers():
    for manager in managers:
        manager.update()