from __future__ import annotations
from typing import Callable, Any
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
    
class ButtonClick:
    
    pass_args: list[Any] = []
    
    def __init__(self, pin: int, event_type: int = GPIO.FALLING, debounce_time_ms: int = 50, multiple_clicks_duration_ms: int = 300) -> None:
        self.pin = pin
        self.event_type = event_type
        self.debounce_time_ms = debounce_time_ms
        self.multiple_clicks_duration_ms = multiple_clicks_duration_ms
        self.last_click_time = 0.0
        self.num_clicks = 0
    
    # decorator
    def __call__(self, callback: Callable[[int], None]) -> Callable[[int], None]:
        def event_handler(_):
            current_time = time.time()

            if self.num_clicks == 0:
                self.num_clicks = 1
            else:
                time_elapsed = current_time - self.last_click_time

                if time_elapsed <= self.multiple_clicks_duration_ms:
                    self.num_clicks += 1
                else:
                    callback(*self.pass_args, self.num_clicks)
                    self.num_clicks = 0

            self.last_click_time = current_time
        
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        GPIO.add_event_detect(
            self.pin,
            self.event_type,
            callback = event_handler,
            bouncetime = self.debounce_time_ms
        )
        
        return event_handler