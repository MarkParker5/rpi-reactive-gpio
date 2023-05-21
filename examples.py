import time
import RPi.GPIO as GPIO
from rpi_reactive_gpio.leds import LedManager, RGBLedManager


def test_all_pins():
    global managers
    pins: list[int] = []
    
    for manager in managers:
        if isinstance(manager, RGBLedManager):
            pins.append(manager.red_pin)
            pins.append(manager.green_pin)
            pins.append(manager.blue_pin)
        elif isinstance(manager, LedManager):
            pins.append(manager.pin)
            
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
        
    time.sleep(0.5)
    
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.LOW)
