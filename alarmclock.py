import internal.notes as notes
import internal.alarm as alarm
import external.weather_api as weather_api
import external.alarm_timestamp as alarm_timestamp

from config import WeatherConfig, Config
from hardware import button, display, wake_up_speaker

from datetime import datetime, timedelta
import time


class AlarmClock():
    def __init__(self):
        # Load config
        self._cfg = Config()
        # Initialize display module

        self.display = display.Display(
            self._cfg.clock_pin,
            self._cfg.dio_pin
        )

        # Initialize button modules
        self.mode_button = button.Button(self._cfg.button_1_pin)
        self.option1_button = button.Button(self._cfg.button_2_pin)
        self.option2_button = button.Button(self._cfg.button_3_pin)

        # Initialize the speaker
        self.speaker = wake_up_speaker.WakeUpSpeaker(self._cfg.buzzer_pin)

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
        self.display.clear()


class NormalMode(AlarmClock):
    def __init__(self, alarm: alarm.Alarm):
        super().__init__()
        self.alarm = alarm
        self.weather_api = weather_api.Location(
            WeatherConfig.weather_api_key,
            WeatherConfig.latitude,
            WeatherConfig.longitude,
        )
        self._temp_display_until = None
        self._showing_outside_temp = False
        self._showing_inside_temp = False

    def refresh_display(self):
        try:
            if (
                self._temp_display_until is not None and
                datetime.now() < self._temp_display_until
            ):
                if self._showing_outside_temp:
                    self.display.update_content(self.weather_api.get_weather())
                elif self._showing_inside_temp:
                    self.display.update_content("0000")
            else:
                self._temp_display_until = None
                self._showing_outside_temp = False
                self._showing_inside_temp = False
                self.display.update_content(
                    self.current_time.get_current_with_refresh()
                )
            self.display.render()
        except Exception as e:
            print(f"Could not refresh display: {e}")

    def mode_button_event(self, event):
        try:
            if event == 'hold':
                print("hold in normal mode")
                return AdjustAlarmMode(self.alarm)
            elif event == 'press':
                print("pressed in normal mode - cycling brightness")
                self.display.cycle_brightness()
            elif event == 'alarm_trigger':
                return AlarmBeepingMode(self.alarm)
        except Exception as e:
            print("something went wrong", e)
        return self

    def aux1_button_event(self, arg):
        self._showing_outside_temp = True
        self._showing_inside_temp = False
        self._temp_display_until = datetime.now() + timedelta(seconds=5)

    def aux2_button_event(self, arg):
        self._showing_inside_temp = True
        self._showing_outside_temp = False
        self._temp_display_until = datetime.now() + timedelta(seconds=5)


class AdjustAlarmMode(AlarmClock):

    def __init__(self, alarm: alarm.Alarm):
        super().__init__()
        self.alarm = alarm
        if not self.alarm.is_active:
            self.alarm.timestamp.refresh_current()
        self._render_cooldown_ms = 500
        self._last_empty_render = datetime.now()
        self._empty_display = False

        self.blink_count = 0

    def refresh_display(self):
        try:
            
            # Blink rapidly 5 times to indicate
            # that we've entered the alarm adjustment mode
            if self.blink_count < 5:
                self.display.clear()
                self.blink_count+=1

            self.display.update_content(self.alarm.timestamp.get_display_string())

            self.display.render()
        except Exception as e:
            print(f"Could not refresh display: {e}")

    def mode_button_event(self, event):
        if event == 'hold':
            print("hold in alarmadjustmode")
            return NormalMode(self.alarm)
        elif event == 'press':
            self.alarm.toggle_alarm()

        return self

    def aux1_button_event(self, arg):
        print(f"increase alarm timestamp to -> {self.alarm.timestamp}")
        self.alarm.increase_timestamp()
        self.refresh_display()

    def aux2_button_event(self, arg):
        print(f"decrease alarm timestamp to -> {self.alarm.timestamp}")
        self.alarm.decrease_timestamp()
        self.refresh_display()


class AlarmBeepingMode(AlarmClock):

    def __init__(self, alarm: alarm.Alarm):
        super().__init__()
        self.alarm = alarm
        self._original_timestamp_hour = alarm.timestamp.timestamp.hour
        self._original_timestamp_minute = alarm.timestamp.timestamp.minute
        self._snooze_minutes = 2

    def mode_button_event(self, event):
        if event == 'press':
            print("press in alarmbeepingmode - dismissing alarm")
            now = datetime.now()
            new_ts = now.replace(
                hour=self._original_timestamp_hour,
                minute=self._original_timestamp_minute,
                second=0
            ) + timedelta(days=1)
            self.alarm.timestamp.timestamp = new_ts
            print(f"alarm has been scheduled to {self.alarm.timestamp}")
            return NormalMode(self.alarm)
        elif event == 'alarm_trigger':
            return self._run_alarm_sequence()
        return self

    def aux1_button_event(self, arg):
        print("aux1 button event in alarmbeepingmode")
        self._snooze()

    def aux2_button_event(self, arg):
        print("aux2 button event in alarmbeepingmode")
        self._snooze()

    def _snooze(self):
        self.alarm.timestamp.timestamp += timedelta(minutes=self._snooze_minutes)
        print(f"snoozing -> new alarmtimestamp is {self.alarm.timestamp}")

    def _run_alarm_sequence(self):
        # This runs a loop inside the normal alarmclock loop until broken.
        alarm_acknowledged = False
        while not alarm_acknowledged:
            # Check if the button has been pressed between each note
            for note, duration in notes.fur_elise:

                if self.option1_button.is_pressed():
                    self.aux1_button_event(None)
                    return NormalMode(self.alarm)

                if self.option2_button.is_pressed():
                    self.aux2_button_event(None)
                    return NormalMode(self.alarm)

                if self.mode_button.is_pressed():
                    alarm_acknowledged = True
                    break

                if note == 0:
                    self.speaker.stop()
                else:
                    self.speaker.play_note(note, duration)

        return self.mode_button_event('press')
