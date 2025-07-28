import RPi.GPIO as GPIO


class Button():

    def __init__(self, pin):
        self.pin = pin
        self._setin()
        self.long_press_treshold = 5

    def _setin(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def add_event(self, func):
        GPIO.add_event_callback(self.pin, func)

    def is_high(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def is_low(self):
        return GPIO.input(self.pin) == GPIO.LOW
