import usocket as socket
import struct
import time

from datetime import date, datetime, timedelta

_tz = {
	"CEST": +2, # Summetime
	"CET": +1
}


"""
Ntp fetches the current time from host upon initialization.
"""
class Ntp():
	def __init__(self, host):
		
		# Fetch UTC time from NTP server
		self.current_time = time.gmtime(
			self.fetch_current_time(host)
        )
		self.adjust_for_daylight_savings()
		print("time received from NTP: ", self.timestamp())
		
	def year(self):
        #     year includes the century (for example 2014).
		return self.current_time[0]
        
	def month(self):
        #     month is 1-12
		return self.current_time[1]
	def week(self):
		return self.current_time[6]
	
	def monthday(self):
        #     monthday is 1-31
		return self.current_time[2]
	
	def hour(self):
        #     hour is 0-23
		return self.current_time[3]

	def minute(self):
        #     minute is 0-59
        # TODO: Add left padding
		return self.current_time[4]
	
	def second(self):
        #     second is 0-59
		return self.current_time[5]
	
	def weekday(self):
        #     weekday is 0-6 for Mon-Sun
		return self.current_time[6]
	
	def yearday(self):
        #     yearday is 1-366
		return self.current_time[7]
	
	def timestamp(self):
		return f"{self.year()}/{self.month()}/{self.monthday()} {self.hour()}:{self.minute()}:{self.second()} weekday: {self.weekday()}"

	def _is_sunday(self, year, month, day) -> bool:
		t = (year, month, day, 0, 0, 0, 0, 0)
		return time.localtime(time.mktime(t))[6] == 6

	"""
		_sunday returns a sunday as a epoch timestamp
	"""	
	def _sunday(self, year, month, day) -> int:
		yearday = date(year, month, day).timetuple()[-2]
		return time.mktime((
			year,
			month,
			day,
			0, # hour
			0, # minute
			0, # seconds
			6, # weekday
			yearday,
        ))

	"""
		_last_sunday_in_march returns the current year's last sunday in March as a Datetime object
	"""
	def _last_sunday_in_march(self) -> int:
		# Loop trough the last week in march and find sunday
		year = self.year()
		for day in range(31, 24, -1):
			if self._is_sunday(year, 3, day):
				return int(self._sunday(
					year, 3, day
				))
		return 0

	"""
		_last_sunday_in_march returns the current year's last sunday in October as a Datetime object
	"""
	def _last_sunday_in_october(self) -> int:
		# Loop trough the last week in october and find sunday
		year = self.year()
		for day in range(31, 24, -1):
			if self._is_sunday(year, 10, day):
				return int(self._sunday(
					year, 10, day
				))
		return 0

	def adjust_for_daylight_savings(self):
		new_ts = time.mktime(self.current_time)
		current_epoch = time.mktime(self.current_time)
		if current_epoch > self._last_sunday_in_march() and current_epoch < self._last_sunday_in_october():
			new_ts += _tz["CEST"] * 3600
		else:	
			new_ts += _tz["CET"] * 3600
		self.current_time = time.localtime(new_ts)
			
		
	def fetch_current_time(self, NTP_HOST: str) -> int:
		# Used to convert the received transmit_timestamp to unix time.
		NTP_DELTA = 2208988800
		# Create a 48 byte packet
		NTP_QUERY = bytearray(48)
		# First byte (LI=0, VN=3, Mode=3 for client mode)
		NTP_QUERY[0] = 0x1B
		
		UNIX_TIME=""
		# Set the target address and port
		addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
		# Create a datagram UDP socket
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			s.settimeout(1)
			s.sendto(NTP_QUERY, addr)
			msg = s.recv(48)

			print(f"Response recieved: {msg}")
			# The response is also a 48 byte packet where the last 8 bytes contain the "transmit timestamp"
			transmit_timestamp = struct.unpack("!I", msg[40:44])[0]

			# TODO: what does the transmit timestmap mean?
			print(f"Transmit timestamp: {transmit_timestamp}")
			UNIX_TIME = transmit_timestamp - NTP_DELTA

		except socket.timeout:
			print("Timeout: No response from NTP server")
		except Exception as e:
			print(f"Error occurred: {e}")
		finally:
			s.close()

		return UNIX_TIME
	

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

    def decrease_minute(self):
        now = datetime.now()

        new_timestamp = self.timestamp - timedelta(minutes=1)

        if new_timestamp.hour * 60 + new_timestamp.minute < now.hour * 60 + now.minute:
            new_date = now + timedelta(days=1)
            self.timestamp = self.timestamp.replace(
                year=new_date.year, month=new_date.month, day=new_date.day
            )
        else:
            self.timestamp = new_timestamp

    # adjusts the timestamp to one day in the future if
    # the current timestamp is less than datetime.now()
    def adjust_for_future(self):
        now = datetime.now()

        ts = self.timestamp

        ts_minutes = ts.hour * 60 + ts.minute
        now_minutes = now.hour * 60 + now.minute

        # Determine if timestamp is in the past, today, or future (by day)
        if ts.date() > now.date():
            if ts_minutes < now_minutes:
                # Future day, earlier time → do nothing
                return
            else:
                # Future day, later time → set to today
                self.timestamp = self.timestamp.replace(
                    year=now.year, month=now.month, day=now.day
                )
                return

        elif ts.date() < now.date():
            if ts_minutes < now_minutes:
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
        if ts_minutes < now_minutes:
            # Still today, but earlier than now → bump to tomorrow
            new_date = now + timedelta(days=1)
            self.timestamp = self.timestamp.replace(
                year=new_date.year, month=new_date.month, day=new_date.day
            )

    def get_current(self):
        return self.get_display_string()

    def get_current_with_refresh(self):
        self.refresh_current()
        return self.get_display_string()

    def get_display_string(self):
        return f"{self.timestamp.hour:0>2}{self.timestamp.minute:0>2}"

    def reset_seconds(self):
        self.timestamp = self.timestamp.replace(second=0)

    def __str__(self):
        return f"{self.timestamp.year}-{self.timestamp.month:0>2}-{self.timestamp.day:0>2} {self.timestamp.hour:0>2}:{self.timestamp.minute:0>2}"

    def get_display_string(self):
        return f"{self.timestamp.hour:0>2}{self.timestamp.minute:0>2}"

    def __eq__(self, other):
        return other.timestamp == self.timestamp

    def __gt__(self, other):
        return self.timestamp > other.timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def refresh_current(self):
        self.timestamp = datetime.now()

    def __repr__(self):
        return self.__str__()
	

if __name__ == "__main__":
	now = Ntp(host="pool.ntp.org")

	# In UTC format
	print("UNIX timestamp recieved from NTP: ", time.mktime(now.current_time))
	print("8-tuple format: ", now.current_time)
	# Adjust for current timezone
	print("timestamp after timezone adjustment (winter time)")
	# Expect 1 hour shift since its currenly january
	now.adjust_for_daylight_savings()
	print(now.current_time)

	# Adjust the date to test summertime as well
	print("adjust timestamp to timestamp (summertime)")
	now.current_time = time.gmtime(1753213285)
	print("before summertime adjustment")
	print(now.current_time)

	now.adjust_for_daylight_savings()
	print("after summertime adjustment")
	print(now.current_time)
