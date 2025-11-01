import usocket as socket
import struct
import time
import machine

from config import NetworkConfig

_tz = {
	"CEST": +2, # Summetime
	"CET": +1
}

"""
Datetime is my own implementation to work with timestamps. Its larges unit is years and smallest is minutes.
"""
class Datetime():
	def __init__(self, 
			  year=None, month=None, day=None, 
			  hour=None, minute=None, seconds=None,
			  subseconds=None, weekday=None, yearday=None):

		self.year       = year
		self.month      = month
		self.day        = day
		self.hour       = hour
		self.minute     = minute
		self.seconds    = seconds
		self.subseconds = subseconds
		self.weekday    = weekday
		self.yearday    = yearday

	def __lt__(self, other):
		self_unix = time.mktime(self.date())

	def __gt__(self, other):
		pass

	def replace(self, 
			 year=None, month=None, day=None, 
			 hour=None, minute=None, seconds=None,
			 subseconds=None, weekday=None, yearday=None):
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
		if seconds != None:
			self.seconds = minute
		if subseconds != None:
			self.subseconds = minute
		if weekday != None:
			self.weekday = minute
		if yearday != None:
			self.yearday = minute

	def date(self):
		# Required format (year, month, mday, hour, minute, second, weekday, yearday)
		return (
			self.year, self.month, self.day, self.hour, self.minute,
			self.seconds, self.subseconds, self.weekday, self.yearday
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
			seconds=0,
			subseconds=0,
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
		for day in range(31, 24, -1):
			if self._is_sunday(self.year, 10, day):
				return self._sunday(
					self.year, 10, day
				)

	def adjust_for_daylight_savings(self):
		if self.__gt__(self._last_sunday_in_march()) and self.__lt__(self._last_sunday_in_october):
			# This means that we are in summertime (CEST)

	def now(self, use_ntp=False):
		# Reset time
		self.year    = None
		self.month   = None
		self.day     = None
		self.hour    = None
		self.minute  = None
		self.weekday = None

		# Update time
		if use_ntp:
			unix_ts = self._get_ntp_time_unix(NetworkConfig.ntp_server)

			# (year, month, mday, hour, minute, second, weekday, yearday)
			t = time.gmtime(unix_ts)
			self.year, self.month, self.day, self.hour, self.minute, self.second, self.weekday, _ = t
			# Adjust for timezone
			self.hour += self.tz

		else:
			# (year, month, day, weekday, hours, minutes, seconds, subseconds)
			t = machine.RTC().datetime()
			self.year, self.month, self.day, self.weekday, self.hour, self.minute, self.seconds, self.subseconds = t
		
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
		except socket.timeout:
			print("Timeout: No response from NTP server")
		except Exception as e:
			print(f"Error occurred: {e}")
		finally:
			s.close()

		return UNIX_TIME
	

if __name__ == "__main__":
	# Example output:
	# Response recieved: b'\x1c\x02\x03\xe8\x00\x00\x03q\x00\x00\x01*g\xb7\xb2\x8c\xec\xa8\xf7\x8b\x7f\x89\xb3_\x00\x00\x00\x00\x00\x00\x00\x00\xec\xa8\xf7\xe5\xee\x07]\xfa\xec\xa8\xf7\xe5\xee\t\xd4j'
	# Transmit timestamp: 3970496485
	# UNIX time: 1761507685
	# According to NTP:
	# time is now: (2025, 10, 26, 20, 41)
	# in an hour its is: (2025, 10, 26, 21, 41)
	# tomorrow is: (2025, 10, 27, 21, 41)

	# GMT+1
	now = Datetime(tz=1)
	now.now(use_ntp=True)

	print("According to NTP:")
	print(f"time is now: {now.date()}")

