from machine import Pin

class Button():

    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, pull=Pin.PULL_DOWN)

    def is_high(self):
        # If the button is not working
        # then I misunderstood the SDK
        return self.pin.value() == 1

    def is_low(self):
        # If the button is not working
        # then I misunderstood the SDK
        return self.pin.value() == 0
