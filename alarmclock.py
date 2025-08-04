from config import WeatherConfig, Config
from hardware import button, display, wake_up_speaker
from external import weather_api, alarm_timestamp
from datetime import datetime, timedelta
from internal import alarm
from notes import fur_elise


# Set the as globals because we do not want to initialize the GPIO pins
# each time the state machine switches state
# (NormalMode -> AlarmAdjustMode -> ...).
CONFIG = Config()
SPEAKER = wake_up_speaker.WakeUpSpeaker(Config().buzzer_pin)
MODE_BUTTON = button.Button(CONFIG.button_1_pin)
OPTION_1_BUTTON = button.Button(CONFIG.button_2_pin)
OPTION_2_BUTTON = button.Button(CONFIG.button_3_pin)

class AlarmClock():
    def __init__(self):
        # Load config
        self._cfg = Config()
        # Initialize display module
        self.display = display.Display(
            self._cfg.segment_pins,
            self._cfg.digit_pins,
        )
        # Initialize button modules
        self.mode_button = MODE_BUTTON
        self.option1_button = OPTION_1_BUTTON
        self.option2_button = OPTION_2_BUTTON

        # Initialize the speaker
        self.speaker = SPEAKER

        # Initialize time
        self.current_time = alarm_timestamp.AlarmTimestamp()

        # Initialize alarm
        self.alarm = alarm.Alarm()

        # Controls content of the display (flashing)
        # TODO: This is reused by multiple children and not alarmclock logic. Perhaps move this into display or create a seperate class?
        self._render_cooldown = 0.5
        self._last_empty_render = datetime.now()
        self._empty_display = False

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

    def cleanup(self):
        self.speaker.close()


class NormalMode(AlarmClock):
    def __init__(self, alarm: alarm.Alarm):
        super().__init__()
        self.alarm = alarm
        self.weather_api = weather_api.Location(
            WeatherConfig.weather_api_key,
            WeatherConfig.latitude,
            WeatherConfig.longitude,
        )

    def refresh_display(self):
        alarm_dot = None
        try:
            if self.alarm.is_active:
                alarm_dot = 3

            self.display.update_content(
                self.current_time.get_current_with_refresh()
            )
            self.display.render(alarm_dot)
        except Exception as e:
            print(f"Could not refresh display: {e}")

    def mode_button_event(self, event):
        if event == 'hold':
            return AdjustAlarmMode(self.alarm)
        elif event == 'press':
            self.current_time.refresh_current()
            return self.current_time.get_current_with_refresh()
        elif event == 'alarm_trigger':
            return AlarmBeepingMode(self.alarm)
        return self

    def aux1_button_event(self, arg):
        self.display.update_content(self.weather_api.get_weather())
        while self.option1_button.is_high():
            self.display.render()

    def aux2_button_event(self, arg):
        # TODO: implement
        self.display.update_content("9999")
        while self.option1_button.is_high():
            self.display.render()


class AdjustAlarmMode(AlarmClock):

    def __init__(self, alarm: alarm.Alarm):
        super().__init__()
        self.alarm = alarm
        self._render_cooldown = 0.5
        self._last_empty_render = datetime.now()
        self._empty_display = False

    def refresh_display(self):
        try:
            if (
                datetime.now() - self._last_empty_render >=
                timedelta(seconds=self._render_cooldown)
            ):
                self._empty_display = not self._empty_display
                self._last_empty_render = datetime.now()

            if self._empty_display:
                self.display.update_content("    ")
            else:
                self.display.update_content(self.alarm.timestamp.get_current())

            dot_num = None
            if self.alarm.is_active:
                dot_num = 3

            self.display.render(dot_num)
        except Exception as e:
            print(f"Could not refresh display: {e}")

    def mode_button_event(self, event):
        if event == 'hold':
            return NormalMode(self.alarm)
        elif event == 'press':
            self.alarm.toggle_alarm()

        return self

    def aux1_button_event(self, arg):
        self.alarm.increase_timestamp()
        self.refresh_display()

    def aux2_button_event(self, arg):
        self.alarm.decrease_timestamp()
        self.refresh_display()


class AlarmBeepingMode(AlarmClock):

    def __init__(self, alarm: alarm.Alarm):
        super().__init__()
        self.alarm = alarm

    def mode_button_event(self, event):
        if event == 'press':
            return NormalMode(self.alarm)
        elif event == 'alarm_trigger':
            return self._run_alarm_sequence()
        return self

    def aux1_button_event(self, arg):
        return NormalMode(alarm)

    def aux2_button_event(self, arg):
        return NormalMode(alarm)

    def _run_alarm_sequence(self) -> NormalMode:
        alarm_acknowledged = False
        while not alarm_acknowledged:
            # Check if the button has been pressed between each note
            for note, duration in fur_elise:
                # When any of the buttons are pressed while in AlarmBeepingMode
                # alarm_acknowledged is set to true.
                if (
                    self.option1_button.is_high() or
                    self.option2_button.is_high() or
                    self.mode_button.is_high()
                ):
                    alarm_acknowledged = True
                    break
                if note == 0:
                    self.speaker.stop()
                else:
                    self.speaker.play_note(note, duration)

        self.alarm.timestamp.adjust_for_future()
        print(self.alarm.timestamp.__repr__())
        return self.mode_button_event('press')
