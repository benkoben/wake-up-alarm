import time

from hardware import button
from config import WeatherConfig
from external import weather_api


def current_time():
    return time.ctime()[11:13] + time.ctime()[14:16]


"""
ButtonDeck defines the state of a button configuration.
This is useful because we need to alter button behaviours based on events.
"""
class ButtonDeck():
    def __init__(self, mode_pin, aux1_pin, aux2_pin):
        self.mode_button = button.Button(mode_pin)
        self.aux1_button = button.Button(aux1_pin)
        self.aux2_button = button.Button(aux2_pin)

    def mode_button_event(event):
        pass

    def aux1_event(self, arg):
        pass

    def aux2_event(self, arg):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class NormalMode(ButtonDeck):
    def __init__(self, mode_pin, aux1_pin, aux2_pin):
        super().__init__(mode_pin, aux1_pin, aux2_pin)

        self.weather_api = weather_api.Location(
            WeatherConfig.weather_api_key,
            WeatherConfig.latitude,
            WeatherConfig.longitude,
        )

    def mode_button_event(self, event):
        if event == 'hold':
            return AdjustAlarmMode(
                    self.mode_button.pin,
                    self.aux1_button.pin,
                    self.aux2_button.pin,
            )
        elif event == 'press':
            return current_time()
        return self

    def aux1_event(self, arg):
        return self.weather_api.get_weather()

    def aux2_event(self, arg):
        # TODO: implement
        return "2002"


class AdjustAlarmMode(ButtonDeck):
    def __init__(self, mode_pin, aux1_pin, aux2_pin):
        super().__init__(mode_pin, aux1_pin, aux2_pin)

        # TODO: Read the set alarm
        self.set_alarm = " 0FF"

    def _get_set_time(self):
        return self.set_alarm

    def mode_button_event(self, event):
        if event == 'hold':
            return NormalMode(
                    self.mode_button.pin,
                    self.aux1_button.pin,
                    self.aux2_button.pin,
            )
        elif event == 'press':
            return self.set_alarm
        return self

    def aux1_event(self, arg):
        return "1001"

    def aux2_event(self, arg):
        return "1002"
