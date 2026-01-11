from machine import Pin
import time

from hardware import digit
from hardware import shift_register
from hardware import numberz


class Display(shift_register.ShiftRegister):

    def __init__(self, digit_pins: list, colon_switch_pin: int, colon_pwr_pin: int, serial_pin: int, clock_pin: int, latch_pin: int):
        super().__init__(serial_pin, clock_pin, latch_pin)

        if len(digit_pins) > 4:
            raise Exception("digit_pins cannot be more than 4 in length")
        
        if len(digit_pins) == 0:
            raise Exception("digit_pins must be provided")

        # will contain four numberz.Number
        self.content = []

        self._sub_content_active = False

        # GPIO ports for each of the digit cathodes
        self._digits = (
            digit.Digit(digit_pins[0]),  # Left
            digit.Digit(digit_pins[1]),  # Middle left
            digit.Digit(digit_pins[2]),  # Middle right
            digit.Digit(digit_pins[3])   # Right
        )

        self.colon_switch = Pin(colon_switch_pin, Pin.OUT)
        self.colon_pwr = Pin(colon_pwr_pin, Pin.OUT)
        self.colon_pwr.high()
        self.colon_switch.high()

    def update_content(self, content: str):
        # Doing alarm logic in a generic class is not the best design
        # but its works for now.
        if len(content) > 4:
            raise Exception("content cannot exceed lenght of 4")
        
        self.content = []
        for c in content:
            if not c.isdigit():
                raise Exception("content must be a number")

            self.content.append(numberz.Number(int(c)))

    def enable_dot_on(self, digit_index: int):
        # is a no-op if digit_index > 3
        if digit_index <= 3:
            if isinstance(self.content[digit_index], numberz.Number):
                self.content[digit_index].enable_dot()

    def disable_dot_on(self, digit_index: int):
        # is a no-op if digit_index > 3
        if digit_index <= 3:
            if isinstance(self.content[digit_index], numberz.Number):
                self.content[digit_index].enable_dot()

    def render(self):
        for i, num in enumerate(self.content):
            for digit in self._digits:
                digit.turn_off()
            
            value = num.value
            self.write(value)
            self._digits[i].turn_on()

        for digit in self._digits:
            digit.turn_off()

        

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
