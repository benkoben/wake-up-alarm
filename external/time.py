import usocket as socket
import struct
import time
import machine

from config import NetworkConfig

_tz = {
	"CEST": 2, # Summetime
	"CET": 1
}

"""
Datetime is my own implementation to work with timestamps. Its larges unit is years and smallest is minutes.
"""
class Datetime():
	def __init__(self, 
			  year=None, month=None, day=None, 
			  hour=None, minute=None, second=None,
			  subsecond=None, weekday=None, yearday=None):

		self.year       = year
		self.month      = month
		self.day        = day
		self.hour       = hour
		self.minute     = minute
		self.second    = second
		self.subsecond = subsecond
		self.weekday    = weekday
		self.yearday    = yearday

	def __lt__(self, other: Datetime) -> bool:
		self_unix = time.mktime(self.date())
		other_unix = time.mktime(other.date())
		return self_unix < other_unix

	def __gt__(self, other: Datetime) -> bool:
		print(self.date())
		self_unix = time.mktime(self.date())
		other_unix = time.mktime(other.date())
		return self_unix > other_unix
	
	def __sub__(self, other: Datetime) -> TimeDelta:
		# TODO - Implement this
		pass

	def __add__(self, other: Datetime) -> TimeDelta:
		# TODO: Implement this
		pass

	def replace(self, 
			 year=None, month=None, day=None, 
			 hour=None, minute=None, second=None,
			 subsecond=None, weekday=None, yearday=None):
		if year != None:
			self.year = year
		if month != None:
			self.month = month
		if day != None:
			self.day = day
		if hour != None:
			self.hour = hour
		if minute != None:
			self.minute = minute
		if second != None:
			self.second = minute
		if subsecond != None:
			self.subsecond = minute
		if weekday != None:
			self.weekday = minute
		if yearday != None:
			self.yearday = minute

	def date(self):
		# Required format (year, month, mday, hour, minute, second, weekday, yearday)
		return (
			self.year, self.month, self.day, self.hour, self.minute,
			self.second, self.subsecond, self.weekday, self.yearday
		)
	
	def tomorrow(self):
		self.replace(day=self.day + 1)
		self.date()

	def _is_sunday(self, year, month, day) -> bool:
		t = (year, month, day, 0, 0, 0, 0, 0)
		return time.localtime(time.mktime(t))[6] == 6

	"""
		_sunday returns a sunday as a Datetime object for given year, month and day
	"""	
	def _sunday(self, year, month, day) -> Datetime:
		return Datetime(
			year=year,
			month=month,
			day=day,
			hour=0,
			minute=0,
			second=0,
			subsecond=0,
			weekday=6
		)

	"""
		_last_sunday_in_march returns the current year's last sunday in March as a Datetime object
	"""
	def _last_sunday_in_march(self) -> Datetime:
		# Loop trough the last week in march and find sunday
		for day in range(31, 24, -1):
			if self._is_sunday(self.year, 3, day):
				return self._sunday(
					self.year, 3, day
				)

	"""
		_last_sunday_in_march returns the current year's last sunday in October as a Datetime object
	"""
	def _last_sunday_in_october(self) -> Datetime:
		# Loop trough the last week in october and find sunday
		print(f"finding last sun day in october {self.year}")
		for day in range(31, 24, -1):
			if self._is_sunday(self.year, 10, day):
				print(f"sunday is {self.year, 10, self.day}")
				return self._sunday(
					self.year, 10, day
				)

	def _adjust_for_daylight_savings(self):
		if self > self._last_sunday_in_march() and self < self._last_sunday_in_october():
			# This means that we are in summertime (CEST)
			self.hour += _tz["CEST"]
		else:
			self.hour += _tz["CET"]

	def now(self, use_ntp=False):
		# Reset time
		self.year    = None
		self.month   = None
		self.day     = None
		self.hour    = None
		self.minute  = None
		self.second  = None
		self.subsecond = 0
		self.weekday = None

		# Update time
		if use_ntp:
			unix_ts = self._get_ntp_time_unix(NetworkConfig.ntp_server)

			# (year, month, mday, hour, minute, second, weekday, yearday)
			t = time.gmtime(unix_ts)
			self.year, self.month, self.day, self.hour, self.minute, self.second, self.weekday, self.yearday = t
			self._adjust_for_daylight_savings()

		else:
			# RTC datetime output: (year, month, day, weekday, hours, minutes, second, subsecond)
			t = machine.RTC().datetime()
			self.year, self.month, self.day, self.weekday, self.hour, self.minute, self.second, self.subsecond = t
		
	def _get_ntp_time_unix(self, NTP_HOST: str) -> str:
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
			res = s.sendto(NTP_QUERY, addr)
			msg = s.recv(48)

			print(f"Response recieved: {msg}")
			# The response is also a 48 byte packet where the last 8 bytes contain the "transmit timestamp"
			transmit_timestamp = struct.unpack("!I", msg[40:44])[0]
			print(f"Transmit timestamp: {transmit_timestamp}")
			UNIX_TIME = transmit_timestamp - NTP_DELTA
			print(f"UNIX time: {UNIX_TIME}")
		except OSError as e:
			print(f"OSError happened: {e}")
		except Exception as e:
			print(f"Error occurred: {e}")
		finally:
			s.close()

		return UNIX_TIME
	
class TimeDelta():

	def __init__(self, 
			  year=None, month=None, day=None, 
			  hour=None, minute=None, second=None, 
			  subsecond=None
		) -> None:
		self.year      = year 		or 0
		self.month     = month 		or 0
		self.day 	   = day 		or 0
		self.hour 	   = hour 		or 0
		self.minute    = minute 	or 0
		self.second    = second 	or 0
		self.subsecond = subsecond  or 0

	def seconds(self) -> int:
		# return how many seconds there are in total in self
		SECS_PER_MIN   = 60
		SECS_PER_HOUR  = 3600
		SECS_PER_DAY   = 86400
		SECS_PER_MONTH = 30 * SECS_PER_DAY
		SECS_PER_YEAR  = 365 * SECS_PER_DAY

		out = 0
		out += self.year 	* SECS_PER_YEAR
		out += self.month 	* SECS_PER_MONTH
		out += self.day 	* SECS_PER_DAY
		out += self.hour 	* SECS_PER_HOUR
		out += self.minute 	* SECS_PER_MIN
		out += self.secods
		out += self.subsecond

		return out

	def __ge__(self, other: TimeDelta):
		return other.seconds() >= self.seconds() 

	def __gt__(self, other: TimeDelta):
		return other.seconds() > self.seconds() 

	def __le__(self, other: TimeDelta):
		return other.seconds() <= self.seconds() 

	def __lt__(self, other: TimeDelta):
		return other.seconds() < self.seconds() 

	def __eq__(self, other: TimeDelta):
		return other.seconds() == self.seconds()

	def __ne__(self, other: TimeDelta):
		return other.seconds() != self.seconds()
	

if __name__ == "__main__":
	# GMT+1
	summer_date = Datetime(year=2025, month=7, day=22, hour=17, minute=0, second=0, subsecond=0, weekday=1)
	print(f"A day in summer UTC: {summer_date.date()}")
	# expect time to be 19:00 efter daylight savings adjustment
	summer_date.adjust_for_daylight_savings()

	# Super minimal testing
	if summer_date.hour != 19:
		raise Exception("daylight time adjustment does not work, expected summertime to be adjusted from 17:00 to 19:00")
	else:
		print(f"A day in summer CEST: {summer_date.date()}")

	today = Datetime()
	today.now(use_ntp=True)
	print(f"Time right now is: {today.date()}")

