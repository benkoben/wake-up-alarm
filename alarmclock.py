import internal.notes as notes
import internal.alarm as alarm
import external.weather_api as weather_api
import external.alarm_timestamp as alarm_timestamp

from config import WeatherConfig, Config
from hardware import display, button

from datetime import datetime, timedelta


class AlarmClock():
    def __init__(self):
        # Load config
        self._cfg = Config()
        # Initialize display module

        self.display = display.Display(
            self._cfg.digit_pins,
            self._cfg.colon_switch_pin,
            self._cfg.colon_pwr_pin,
            self._cfg.serial_pin,
            self._cfg.clock_pin,
            self._cfg.latch_pin,
        )
        # Initialize button modules
        self.mode_button = button.Button(self._cfg.button_1_pin)
        self.option1_button = button.Button(self._cfg.button_2_pin)
        self.option2_button = button.Button(self._cfg.button_3_pin)

        # Initialize the speaker
        self.speaker = self._cfg.buzzer_pin

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
        pass


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
            self.display.render()
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
        current_tmp_outside = self.weather_api.get_weather()
        if current_tmp_outside == None:
            current_tmp_outside = "0000"
        self.display.update_content(current_tmp_outside)
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
        self._render_cooldown_ms = 500
        self._last_empty_render = datetime.now()
        self._empty_display = False

    def refresh_display(self):
        try:
            if (
                datetime.now() - self._last_empty_render >=
                timedelta(milliseconds=self._render_cooldown_ms)
            ):
                self._empty_display = not self._empty_display
                self._last_empty_render = datetime.now()

            if self._empty_display:
                self.display.update_content("    ")
            else:
                self.display.update_content(self.alarm.timestamp.get_current())

            self.display.render()
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
        return NormalMode(self.alarm)

    def aux2_button_event(self, arg):
        return NormalMode(self.alarm)

    def _run_alarm_sequence(self):
        alarm_acknowledged = False
        while not alarm_acknowledged:
            # Check if the button has been pressed between each note
            for note, duration in notes.fur_elise:
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
                    pass
                    # self.speaker.stop()
                    # TODO
                else:
                    pass
                    # TODO
                    # self.speaker.play_note(note, duration)

        self.alarm.timestamp.adjust_for_future()
        print(self.alarm.timestamp.__repr__())
        return self.mode_button_event('press')
