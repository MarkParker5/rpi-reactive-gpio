import time
import atexit
import RPi.GPIO as GPIO
from .pin_manager import tick_all_managers, update_all_managers


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def main_loop(update_interval: float = 1.0, ticks_count: int = 100):
    while True:
        update_all_managers()
        for i in range(ticks_count):
            tick_all_managers(i / ticks_count)
            time.sleep(update_interval / ticks_count)
        
@atexit.register
def cleanup():
    GPIO.cleanup()