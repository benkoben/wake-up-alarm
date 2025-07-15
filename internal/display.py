import RPi.GPIO as GPIO
import time

from . import digit

class Display():
    def __init__(self, refresh_rate: float, segment_pins: tuple, digit_pins: tuple):

        if len(segment_pins) > 8:
            raise Exception("segment_pins cannot be more than 8 in length")

        if len(digit_pins) > 4:
            raise Exception("digit_pins cannot be more than 4 in length")

        # GPIO ports for 7 segment of each digit anode
        # 7 seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
        self._sleep = refresh_rate

        # GPIO ports for each of the digit cathodes 
        self._digits = (
            digit.Digit(digit_pins[0], segment_pins), # Left
            digit.Digit(digit_pins[1], segment_pins), # Middle left
            digit.Digit(digit_pins[2], segment_pins), # Middle right
            digit.Digit(digit_pins[3], segment_pins)  # Right
        )
        
        # Set all segments to low
        for segment in segment_pins:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, GPIO.LOW)

    def render(self, input: str):
        
        if len(input) > 4:
            raise Exception("input cannot exceed lenght of 4")

        for n, digit in enumerate(self._digits):
            digit.turn_on()
            digit.display(input[n])

            time.sleep(self._sleep)
            digit.turn_off()

