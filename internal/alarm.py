from datetime import datetime, timedelta


class Alarm():
    def __init__(self):
        self.is_active = False
        self._timestamp = datetime.strptime("0000", "%H%M")

    def get_timestamp(self):
        return self._timestamp.strftime("%H%M")

    def toggle_alarm(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        print(f"alarm is now {self.is_active}")

    def increase_timestamp(self, minutes):
        self._timestamp += timedelta(minutes=minutes)

    def decrease_timestamp(self, minutes):
        self._timestamp -= timedelta(minutes=minutes)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return __class__.__name__
