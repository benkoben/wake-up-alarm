from datetime import datetime, timedelta


class AlarmTimestamp():
    def __init__(self, hour=None, minute=None):
        now = datetime.now()
        if not hour or not minute:
            self.current = now
        else:
            timestamp = f"{now.year}-{now.month}-{now.day} "
            format = "%Y-%m-%d "

            if hour:
                timestamp += hour
                format += "%H"
            if minute:
                timestamp += minute
                format += "%M"

            self.current = datetime.strptime(timestamp, format)

    def increase_minute(self):
        current_day = self.current.day
        self.current += timedelta(minutes=1)
        if self.current.day > current_day:
            self.current -= timedelta(days=1)

    def decrease_minute(self):
        current_day = self.current.day
        self.current -= timedelta(minutes=1)
        if self.current.day < current_day:
            self.current += timedelta(days=1)

    def get_current(self):
        return self.__str__()

    def get_current_with_refresh(self):
        self.refresh_current()
        return self.__str__()

    def __str__(self):
        return datetime.strftime(self.current, "%H%M")

    def __eq__(self, other):
        return other.current == self.current

    def __gt__(self, other):
        return self.current > other.current

    def __lt__(self, other):
        return self.current < other.current

    def refresh_current(self):
        self.current = datetime.now()
