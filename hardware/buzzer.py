import RPi.GPIO as GPIO
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone


class ActiveBuzzer(TonalBuzzer):

    def __init__(self, pin):
        super().__init__(pin)

    # def load_sound(self, func):
    #   GPIO.add_event_callback(self.pin, func)

    def is_high(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def is_low(self):
        return GPIO.input(self.pin) == GPIO.LOW


if __name__ == "__main__":
    import time

    GPIO.setmode(GPIO.BCM)
    pin = 21

    buzzer = ActiveBuzzer(pin)

    # Define a list of notes and their durations (in seconds)
    notes = [
    (659.25, 0.4),  # E5
    (622.25, 0.4),  # D#5
    (659.25, 0.4),  # E5
    (622.25, 0.4),  # D#5
    (659.25, 0.4),  # E5
    (493.88, 0.4),  # B4
    (587.33, 0.4),  # D5
    (523.25, 0.4),  # C5
    (440.00, 0.9),  # A4


    (349.23, 0.4),  # F4
    (440.00, 0.4),  # A4
    (493.88, 0.6),  # B4
    (0, 0.3),       # rest
    (349.23, 0.4),  # F4
    (440.00, 0.4),  # A4
    (493.88, 0.6),  # B4

    (392.00, 0.4),  # G4
    (0, 0.1),       # rest
    (659.25, 0.4),  # E5
    (622.25, 0.4),  # D#5
    (659.25, 0.4),  # E5
    (622.25, 0.4),  # D#5
    (659.25, 0.4),  # E5
    (493.88, 0.4),  # B4
    (587.33, 0.4),  # D5
    (523.25, 0.4),  # C5
    (440.00, 0.8),  # A4

    (349.23, 0.4),  # F4
    (440.00, 0.4),  # A4
    (493.88, 0.6),  # B4
    (0, 0.3),       # rest


    (523.25, 0.4),  # C5
    (493.88, 0.4),  # B4
    (440.00, 0.8),  # A4
    ]

    # Play each note
    while True:
        for note, duration in notes:
            if note == 0:
                buzzer.stop()
            else:
                buzzer.play(note)
            time.sleep(duration)
