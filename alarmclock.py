import time
import buttons
import RPi.GPIO as GPIO

from hardware import display
from config import Config
from datetime import datetime


class Alarmclock():
    def __init__(self):
        self._alarm_time = ""
        self._alarm_mode_active = False
        self._cfg = Config()

        self._display = display.Display(
            self._cfg.segment_pins,
            self._cfg.digit_pins,
        )

        self.buttons = buttons.NormalMode(
            self._cfg.button_1_pin,
            self._cfg.button_2_pin,
            self._cfg.button_3_pin,
        )

    def show_time(self):
        return time.ctime()[11:13] + time.ctime()[14:16]

    def get_alarm_time(self) -> str:
        if self._alarm_time == "":
            return " 0FF"

        return self._alarm_time

    def set_alarm_time(self):
        # Open a new buffer that shows time, starting from 0000
        while True:
            pass

    # start runs the alarm clock's main control loop
    def start(self):
        while True:

            if self.buttons.mode_button.is_high():
                count = datetime.now()
                while self.buttons.mode_button.is_high():
                    self._display.update_content(
                        self.buttons.mode_button_event('press'),
                    )
                    self._display.render()

                    if (datetime.now() - count).seconds == 3:
                        # switch state
                        self.buttons = self.buttons.mode_button_event('hold')
                        print(f"switched mode to {self.buttons}")
                        time.sleep(1)

                self._alarm_mode_active = False

            if self.buttons.aux1_button.is_high():
                self._display.update_content(
                    self.buttons.aux1_event(None)
                )
                self._display.render()
                continue

            if self.buttons.aux2_button.is_high():
                self._display.update_content(
                    self.buttons.aux2_event(None)
                )
                self._display.render()
                continue

            # Render time on module 7 Segment 4 Digit display
            self._display.update_content(self.show_time())
            self._display.render()


if __name__ == "__main__":
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    a = Alarmclock()
    try:
        while True:
            a._display.update_content(" 0FF")
            a._display.render()
    finally:
        GPIO.cleanup()
