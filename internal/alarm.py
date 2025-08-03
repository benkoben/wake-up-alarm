from datetime import timedelta
from external import alarm_timestamp


class Alarm():
    def __init__(self):
        self.is_active = False
        self.timestamp = alarm_timestamp.AlarmTimestamp(
            hour="00",
            minute="00"
        )

    def get_timestamp(self):
        return self.timestamp.get_current()

    def toggle_alarm(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        print(f"alarm is now {self.is_active}")

    def increase_timestamp(self):
        self.timestamp.increase_minute()

    def decrease_timestamp(self):
        self.timestamp.decrease_minute()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return __class__.__name__
