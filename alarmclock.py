import time

from hardware import button, display
from config import WeatherConfig, Config
from external import weather_api
from datetime import datetime, timedelta
from internal import alarm


def current_time():
    return time.ctime()[11:13] + time.ctime()[14:16]


"""
ButtonDeck defines the state of a button configuration.
This is useful because we need to alter button behaviours based on events.
"""
class AlarmClock():
    def __init__(self):
        # Controls which dots to activate
        self._dot_0_active = False
        self._dot_1_active = False
        self._dot_2_active = False
        self._dot_3_active = False
        # Load config
        self._cfg = Config()
        # Initialize display module
        self._display = display.Display(
            self._cfg.segment_pins,
            self._cfg.digit_pins,
        )
        # Initialize button modules
        self.mode_button = button.Button(self._cfg.button_1_pin)
        self.aux1_button = button.Button(self._cfg.button_2_pin)
        self.aux2_button = button.Button(self._cfg.button_3_pin)

        # Initialize alarm
        self.alarm = None
        self.alarm_time = None
        self.alarm_active = False

    def refresh_display(self):
        pass

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


class NormalMode(AlarmClock):
    def __init__(self, alarm):
        super().__init__()
        self.alarm = alarm
        self.weather_api = weather_api.Location(
            WeatherConfig.weather_api_key,
            WeatherConfig.latitude,
            WeatherConfig.longitude,
        )

    def refresh_display(self):
        alarm_dot = None
        if self.alarm.is_active:
            alarm_dot = 3

        self._display.update_content(current_time())
        self._display.render(alarm_dot)

    def mode_button_event(self, event):
        if event == 'hold':
            return AdjustAlarmMode(self.alarm)
        elif event == 'press':
            return current_time()
        return self

    def aux1_event(self, arg):
        self._display.update_content(self.weather_api.get_weather())
        while self.aux1_button.is_high():
            self._display.render()

    def aux2_event(self, arg):
        # TODO: implement
        self._display.update_content("9999")
        while self.aux1_button.is_high():
            self._display.render()


class AdjustAlarmMode(AlarmClock):

    def __init__(self, alarm):
        super().__init__()
        self.alarm = alarm
        self._render_cooldown = 0.5
        self._last_empty_render = datetime.now()
        self._empty_display = False

    def refresh_display(self):

        if datetime.now() - self._last_empty_render >= timedelta(seconds=self._render_cooldown):
            self._empty_display = not self._empty_display
            self._last_empty_render = datetime.now()

        if self._empty_display:
            self._display.update_content("    ")
        else:
            self._display.update_content(self.alarm.get_timestamp())

        dot_num = None
        if self.alarm.is_active:
            dot_num = 3

        self._display.render(dot_num)

    def mode_button_event(self, event):
        if event == 'hold':
            return NormalMode(self.alarm)
        elif event == 'press':
            self.alarm.toggle_alarm()

        return self

    def aux1_event(self, arg):
        self.alarm.increase_timestamp(minutes=1)
        self.refresh_display()

    def aux2_event(self, arg):
        self.alarm.decrease_timestamp(minutes=1)
        self.refresh_display()
