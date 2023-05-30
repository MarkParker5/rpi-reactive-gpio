from __future__ import annotations
from typing import Callable, Any, TypeVar
import time
import RPi.GPIO as GPIO
from .pin_manager import tickables


ButtonCallback = TypeVar('ButtonCallback', bound = Callable[[int], None] | Callable[['ButtonClick', int], None])
    
class ButtonClick:
    
    pass_args: list[Any] = []
    
    def __init__(self, pin: int, event_type: int = GPIO.FALLING, debounce_time_ms: int = 50, multiple_clicks_duration_ms: int = 500) -> None:
        self.pin = pin
        self.event_type = event_type
        self.debounce_time_ms = debounce_time_ms
        self.multiple_clicks_duration_ms = multiple_clicks_duration_ms
        self.last_click_time = 0.0
        self.num_clicks = 0
        
    def tick(self, _):
        if self.num_clicks == 0:
            return
        else:
            time_elapsed = time.time() - self.last_click_time

            if time_elapsed > self.multiple_clicks_duration_ms / 1000:
                self.callback(*self.pass_args, self.num_clicks)
                self.num_clicks = 0
    
    # decorator
    def __call__(self, callback: ButtonCallback) -> ButtonClick:
        self.callback = callback
        
        def event_handler(_):
            self.num_clicks += 1
            self.last_click_time = time.time()
        
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        GPIO.add_event_detect(
            self.pin,
            self.event_type,
            callback = event_handler,
            bouncetime = self.debounce_time_ms
        )
        
        tickables.append(self)
        return self
