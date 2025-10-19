from machine import Pin

class Digit():
    def __init__(self, pin: int):
        self._activation_pin = Pin(pin, Pin.OUT)

    def turn_off(self):
        self._activation_pin.low()

    def turn_on(self):
        self._activation_pin.high()

    # TODO: Clean this up. I will instead be rendering the dots
    # as part of the binary sequence sent into render.
    # def _activate_dot(self):
    #     # It might be a bit confusing but 
    #     # LOW = means that the segment of the digit will be active
    #     # if the digit's cathode is activated.
    #     GPIO.output(25, GPIO.LOW)

    # def _deactivate_dot(self):
    #     # It might be a bit confusing but 
    #     # LOW = means that the segment of the digit will be inactive
    #     # if the digit's cathode is activated.
    #     #
    #     # 25 is the pin used to control the dot
    #     GPIO.output(25, GPIO.HIGH)

    # Renders a number to the digit
    # def display(self, character):
    #     if character not in characters.NUMS.keys():
    #         raise Exception("number cannot be more than 9 or less than 0")

    #     for segment in range(0,7):
    #         GPIO.output(self._segments[segment], self._numbers[character][segment])
    #         GPIO.output(25, GPIO.HIGH)
