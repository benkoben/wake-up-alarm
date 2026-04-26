from machine import Pin
import time

from hardware import tm1637

class Display():
    """
        Display wraps around a TM1637 module to control the content
        and call rendering
    """
    def __init__(self, clock_pin: int, dio_pin: int, brightness=2):

        # will contain four numberz.Number
        self.content = []
        self.brightness = brightness

        self.tm1367 = tm1637.TM1637Display(
                clock_pin,
                dio_pin
        )

        self._sub_content_active = False
    
    """
        Updates the content buffer. Wont show on screen until render is called.
        If content is empty the content buffer is cleared.
    """
    def update_content(self, content: str):
        # Doing alarm logic in a generic class is not the best design
        # but its works for now.
        if len(content) > 4:
            raise Exception("content cannot exceed lenght of 4")
        if len(content) == 0:

            # Do nothing if content is empty
            self.content = []

        self.content = content

    def brightness_up(self):
        self.brightness += 1
        self.tm1367.setBrightness(self.brightness)

    def brightness_down(self):
        self.brightness -= 1
        self.tm1367.setBrightness(self.brightness)

    def cycle_brightness(self):
        self.brightness = (self.brightness + 1) % 3
        self.tm1367.setBrightness(self.brightness)

    def clear(self):
        self.tm1367.clear()

    def render(self):
        try:
            self.tm1367.showNumberDec(int("".join(self.content)))
        except Exception as e:
            print(f"failed to render: Exception: {e}")
        

if __name__ == "__main__":
    digit_pins = [20, 27, 13, 10] # dp1, dp2, dp3, dp4
    serial_pin = 18
    latch_pin = 5
    clock_pin = 14
    colon_switch_pin = 28
    colon_pwr_pin = 16

    example_data = "1337"
    display = Display(digit_pins, colon_switch_pin, colon_pwr_pin, serial_pin, clock_pin, latch_pin)
    display.update_content(example_data)

    print(f"rendering {example_data}")
    while True:
        print(display.content)
        time.sleep_ms(1)
        display.render()
