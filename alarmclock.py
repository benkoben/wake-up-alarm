import time
import RPi.GPIO as GPIO

from hardware import display
from hardware import button
from config import Config, WeatherConfig
from datetime import datetime

from modules import weather_api

class Alarmclock():
    def __init__(self):
        self._alarm_time = ""
        self._alarm_mode_active = False
        self._cfg = Config()
        self._display = display.Display(
            self._cfg.segment_pins,
            self._cfg.digit_pins,
        )

        # Initiatize hardware
        self.mode_button = button.Button(self._cfg.button_1_pin)
        self.increase_button = button.Button(self._cfg.button_2_pin)
        self.decrease_button = button.Button(self._cfg.button_3_pin)

        # Initialize modules
        self.weather_module = weather_api.Location(
            WeatherConfig.weather_api_key,
            WeatherConfig.latitude,
            WeatherConfig.longitude,
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

            if GPIO.input(self.mode_button.pin) == GPIO.HIGH:
                count = datetime.now()

                while GPIO.input(self.mode_button.pin) == GPIO.HIGH:
                    self._display.update_content(
                        self.get_alarm_time(),
                    )
                    self._display.render()
                    if (datetime.now() - count).seconds > 3:
                        self._alarm_mode_active = True
                        print("now in set alarm mode")
                        break
                self._alarm_mode_active = False


            if GPIO.input(self.increase_button.pin) == GPIO.HIGH:
                if not self._alarm_mode_active:
                    self._display.update_content(
                            self.weather_module.get_weather(),
                    )
                    self._display.render()
                    continue
                else:
                    # TODO:  implement alarm decrease
                    pass

            if GPIO.input(self.decrease_button.pin) == GPIO.HIGH:
                print("decrease presssed")

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
