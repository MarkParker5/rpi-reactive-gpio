import time
from raspi_gpio import GPIO
from rpi_reactive_gpio import managers

# test all pins

def test_all_pins():
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


from rpi_reactive_gpio import ButtonClick, LedManager, RGBLedManager, LedState, RGBLedState, main_loop

# Global style

led_mode = 0
color_index = 0
    
@ButtonClick(pin = 5)
def button_click(num_clicks: int):
    global led_mode
    if num_clicks == 1:
        led_mode = int(not bool(led_mode))
    elif num_clicks == 2:
        led_mode = 2
    elif num_clicks == 3:
        led_mode = 3
    else:
        print(f'button2 clicked {num_clicks} times')
    
@ButtonClick(pin = 5, debounce_time_ms = 2000)
def button_long_press(_):
    color_index += 1
    
@LedManager(pin = 29)
def get_led_state() -> LedState:
    global led_mode
    match led_mode:
        case 0:
            return LedState.off
        case 1:
            return LedState.on
        case 2:
            return LedState.blink
        case 3:
            return LedState.fast_blink
    return LedState.off

@RGBLedManager(red_pin = 33, green_pin = 35, blue_pin = 37)
def get_rgb_led_state() -> RGBLedState:
    global color_index
    match color_index % 5:
        case 0:
            return RGBLedState.off
        case 1:
            return RGBLedState.red
        case 2:
            return RGBLedState.yellow
        case 3:
            return RGBLedState.green
        case 4:
            return RGBLedState.blue
    return RGBLedState.off
        
# if __name__ == '__main__':
#     test_all_pins()
#     main_loop()


# OOP style

from rpi_reactive_gpio.scene import Scene


class ExampleScene(Scene):
    
    led_mode = 0
    color_index = 0
        
    @ButtonClick(pin = 5)
    def button_click(self, num_clicks: int):
        if num_clicks == 1:
            self.led_mode = int(not bool(self.led_mode))
        elif num_clicks == 2:
            self.led_mode = 2
        elif num_clicks == 3:
            self.led_mode = 3
        else:
            print(f'button2 clicked {num_clicks} times')
        
    @ButtonClick(pin = 5, debounce_time_ms = 2000)
    def button_long_press(self, _):
        self.color_index += 1
        
    @LedManager(pin = 29)
    def get_led_state(self) -> LedState:
        match self.led_mode:
            case 0:
                return LedState.off
            case 1:
                return LedState.on
            case 2:
                return LedState.blink
            case 3:
                return LedState.fast_blink
        return LedState.off

    @RGBLedManager(red_pin = 33, green_pin = 35, blue_pin = 37)
    def get_rgb_led_state(self) -> RGBLedState:
        match self.color_index % 5:
            case 0:
                return RGBLedState.off
            case 1:
                return RGBLedState.red
            case 2:
                return RGBLedState.yellow
            case 3:
                return RGBLedState.green
            case 4:
                return RGBLedState.blue
        return RGBLedState.off
            
if __name__ == '__main__':
    ExampleScene().main_loop()
