from __future__ import annotations
from enum import Enum
from typing import Callable
import RPi.GPIO as GPIO
from .pin_manager import tickables, managers


class LedState(Enum):
    off = 0
    on = 1
    blink = 2
    fast_blink = 3

class LedManager:
        
    _get_pin_state: Callable[[], LedState]
    _last_led_state: LedState = LedState.off
    
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
    def tick(self, period: float = 1.0):
        '''period must be in range 0.0...1.0'''
        match self._last_led_state:
            case LedState.off:
                GPIO.output(self.pin, GPIO.LOW)
            case LedState.on:
                GPIO.output(self.pin, GPIO.HIGH)
            case LedState.blink:
                GPIO.output(self.pin, GPIO.LOW if period < 0.5 else GPIO.HIGH)
            case LedState.fast_blink:
                GPIO.output(self.pin, GPIO.LOW if period % 0.2 < 0.1 else GPIO.HIGH)
        
    def update(self, *args, **kwargs):
        self._last_led_state = self._get_pin_state(*args, **kwargs)
    
    # decorator
    def __call__(self, get_pin_state: Callable[..., LedState]) -> LedManager:
        global managers
        self._get_pin_state = get_pin_state
        managers.append(self)
        tickables.append(self)
        return self
    
class RGBLedState(Enum):
    off = 0
    red = 1
    yellow = 2
    green = 3
    blue = 4
        
class RGBLedManager:
    
    _get_pin_state: Callable[[], RGBLedState]
    _last_led_state: RGBLedState = RGBLedState.off
    
    def __init__(self, red_pin: int, green_pin: int, blue_pin: int):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)
        GPIO.output(red_pin, GPIO.LOW)
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(blue_pin, GPIO.LOW)
        
    def tick(self, period: float = 1.0):
        '''period must be in range 0.0...1.0'''
        match self._last_led_state:
            case RGBLedState.off:
                GPIO.output(self.red_pin, GPIO.LOW)
                GPIO.output(self.green_pin, GPIO.LOW)
                GPIO.output(self.blue_pin, GPIO.LOW)
            case RGBLedState.red:
                GPIO.output(self.red_pin, GPIO.HIGH)
                GPIO.output(self.green_pin, GPIO.LOW)
                GPIO.output(self.blue_pin, GPIO.LOW)
            case RGBLedState.yellow:
                GPIO.output(self.red_pin, GPIO.HIGH if period < 0.5 else GPIO.LOW)
                GPIO.output(self.green_pin, GPIO.HIGH if period < 0.5 else GPIO.LOW)
                GPIO.output(self.blue_pin, GPIO.LOW)
            case RGBLedState.green:
                GPIO.output(self.red_pin, GPIO.LOW)
                GPIO.output(self.green_pin, GPIO.HIGH)
                GPIO.output(self.blue_pin, GPIO.LOW)
            case RGBLedState.blue:
                GPIO.output(self.red_pin, GPIO.LOW)
                GPIO.output(self.green_pin, GPIO.LOW)
                GPIO.output(self.blue_pin, GPIO.HIGH)
              
    def update(self):
        self._last_led_state = self._get_pin_state()      
          
    # decorator
    def __call__(self, get_pin_state: Callable[..., RGBLedState]) -> RGBLedManager:
        global managers
        self._get_pin_state = get_pin_state
        managers.append(self)
        return self