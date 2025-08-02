import RPi.GPIO as GPIO
import time

from . import digit

_REFRESH_RATE = 0.005


class Display():

    def __init__(self, segment_pins: tuple, digit_pins: tuple):

        if len(segment_pins) > 8:
            raise Exception("segment_pins cannot be more than 8 in length")

        if len(digit_pins) > 4:
            raise Exception("digit_pins cannot be more than 4 in length")

        self.content = ""

        # GPIO ports for 7 segment of each digit anode
        # 7 seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
        self._refresh_rate = _REFRESH_RATE
        self._sub_content_active = False

        # GPIO ports for each of the digit cathodes
        self._digits = (
            digit.Digit(digit_pins[0], segment_pins),  # Left
            digit.Digit(digit_pins[1], segment_pins),  # Middle left
            digit.Digit(digit_pins[2], segment_pins),  # Middle right
            digit.Digit(digit_pins[3], segment_pins)   # Right
        )

        # Set all segments to low
        for segment in segment_pins:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, GPIO.LOW)

    def update_content(self, content: str):
        if len(content) > 4:
            raise Exception("content cannot exceed lenght of 4")
        self.content = content

    def render(self, dot_number=None):

        if dot_number and dot_number > len(self._digits):
            raise Exception(f"dot_number cannot be larger than {len(self._digits)}")

        for n, d in enumerate(self._digits):

            d.turn_on()
            d.display(self.content[n])

            if dot_number is not None and n == dot_number:
                d._activate_dot()

            time.sleep(self._refresh_rate)
            d.turn_off()
