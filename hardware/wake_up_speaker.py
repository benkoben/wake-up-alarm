import RPi.GPIO as GPIO
import time

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone


class WakeUpSpeaker():

    def __init__(self, pin):
        self.buzzer = TonalBuzzer(pin)

    def play_note(self, note, duration):
        try:
            self.buzzer.play(Tone(note))
            time.sleep(duration)
            self.buzzer.stop()
        except Exception as e:
            print(f"Error playing note: {e}")

    def close(self):
        self.buzzer.close()
