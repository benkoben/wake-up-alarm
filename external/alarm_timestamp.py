from datetime import datetime, timedelta


class AlarmTimestamp():
    def __init__(self, hour=None, minute=None):
        now = datetime.now()
        self.timestamp = now
        if hour:
            self.timestamp.replace(hour=hour)
        if minute:
            self.timestamp.replace(minute=minute)

    def increase_minute(self):
        self.timestamp += timedelta(minutes=1)
        self.adjust_for_future()
        print(f"today is: {datetime.now()}")
        print(f"timestamp is now set to: {self.timestamp}")

    def decrease_minute(self):
        self.timestamp -= timedelta(minutes=1)
        self.adjust_for_future()
        print(f"today is: {datetime.now()}")
        print(f"timestamp is now set to: {self.timestamp}")

    # adjusts the timestamp to one day in the future if
    # the current timestamp is less than datetime.now()
    def adjust_for_future(self):
        now = datetime.now()

        ts = self.timestamp

        # Compare only hours and minutes
        ts_hhmmss = ts.hour * 60 + ts.minute * 60 + ts.second
        now_hhmmss = now.hour * 60 + now.minute * 60 + now.second

        # Determine if timestamp is in the past, today, or future (by day)
        if ts.date() > now.date():
            if ts_hhmmss < now_hhmmss:
                # Future day, earlier time → do nothing
                return
            else:
                # Future day, later time → set to today
                self.timestamp = self.timestamp.replace(
                    year=now.year, month=now.month, day=now.day
                )
                return

        elif ts.date() < now.date():
            if ts_hhmmss < now_hhmmss:
                # Past day, earlier time → set to tomorrow
                new_date = now + timedelta(days=1)
                self.timestamp = self.timestamp.replace(
                    year=new_date.year, month=new_date.month, day=new_date.day
                )
                return
            else:
                # Past day, later time → set to today
                self.timestamp = self.timestamp.replace(
                    year=now.year, month=now.month, day=now.day
                )
                return

        # If it's today, and still in the future — leave it alone
        if ts_hhmmss < now_hhmmss:
            # Still today, but earlier than now → bump to tomorrow
            new_date = now + timedelta(days=1)
            self.timestamp = self.timestamp.replace(
                year=new_date.year, month=new_date.month, day=new_date.day
            )

    def get_current(self):
        return self.__str__()

    def get_current_with_refresh(self):
        self.refresh_current()
        return self.__str__()

    def reset_seconds(self):
        self.timestamp = self.timestamp.replace(second=0)
        print(self.__repr__())

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.timestamp.strftime('%Y/%m/%d %H:%M:%S')}"

    def __str__(self):
        return datetime.strftime(self.timestamp, "%H%M")

    def __eq__(self, other):
        return other.timestamp == self.timestamp

    def __gt__(self, other):
        return self.timestamp > other.timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def refresh_current(self):
        self.timestamp = datetime.now()
