import RPi.GPIO as GPIO

from . import numbers

class Digit():
    def __init__(self, pin: int, segments: tuple):
        self._activation_pin = pin
        self._segments = segments
        self._numbers = numbers.NUMS
        self._setout()

    def _setout(self):
        GPIO.setup(self._activation_pin, GPIO.OUT)

    def turn_off(self):
        GPIO.output(self._activation_pin, GPIO.LOW)

    def turn_on(self):
        GPIO.output(self._activation_pin, GPIO.HIGH)

    def _activate_dot(self):
        # It might be a bit confusing but 
        # LOW = means that the segment of the digit will be active
        # if the digit's cathode is activated.
        GPIO.output(25, GPIO.LOW)

    def _deactivate_dot(self):
        # It might be a bit confusing but 
        # LOW = means that the segment of the digit will be inactive
        # if the digit's cathode is activated.
        #
        # 25 is the pin used to control the dot
        GPIO.output(25, GPIO.HIGH)

    # Renders a number to the digit
    def display(self, number):
        if number not in numbers.NUMS.keys():
            raise Exception("number cannot be more than 9 or less than 0")

        for segment in range(0,7):
            GPIO.output(self._segments[segment], self._numbers[number][segment])
            GPIO.output(25, GPIO.HIGH)
