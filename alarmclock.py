import time
import RPi.GPIO as GPIO

from hardware import display
from hardware import button
from config import Config, WeatherConfig

from modules import weather_api

class Alarmclock():
    def __init__(self):
        self.cfg = Config()
        self.display = display.Display(
            self.cfg.segment_pins,
            self.cfg.digit_pins,
        )

        self.button = button.Button(self.cfg.button_1_pin)

        self.weather_module = weather_api.Location(
            WeatherConfig.weather_api_key,
            WeatherConfig.latitude,
            WeatherConfig.longitude,
        )

    def show_time(self):
        return time.ctime()[11:13] + time.ctime()[14:16]

    # start runs the alarm clock's main control loop
    def start(self):
        while True:

            if GPIO.input(self.button.pin) == GPIO.HIGH:
                self.display.update_content(
                        self.weather_module.get_weather(),
                )
                self.display.render()
                continue

            # Render time on module 7 Segment 4 Digit display
            self.display.update_content(self.show_time())
            self.display.render()
