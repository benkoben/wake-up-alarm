import usocket as socket
import struct
import time
import machine

from config import NetworkConfig

"""
Datetime is my own implementation to work with timestamps. Its larges unit is years and smallest is minutes.
"""
class Datetime():
	def __init__(self, tz=1):
		self.year = ""
		self.month = ""
		self.day = ""
		self.hour = ""
		self.minute = ""
		self.tz = tz	

	def replace(self, year=None, month=None, day=None, hour=None, minute=None):
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

	def date(self):
		return (
			self.year,
			self.month,
			self.day,
			self.hour,
			self.minute
		)
	
	def tomorrow(self):
		return (
			self.year,
			self.month,
			self.day + 1,
			self.hour,
			self.minute
		)

	def now(self, use_ntp=False):
		# Reset time
		self.year = None
		self.month = None
		self.day = None
		self.hour = None
		self.minute = None

		# Update time
		if use_ntp:
			unix_ts = self._get_ntp_time_unix(NetworkConfig.ntp_server)
			t = time.gmtime(unix_ts)
			self.year   = t[0]
			self.month  = t[1]
			self.day    = t[2]
			self.hour   = t[3] + self.tz
			self.minute = t[4]

		else:
			t = machine.RTC().datetime()
			self.year   = t[0]
			self.month  = t[1]
			self.day    = t[2]
			self.hour   = t[3]
			self.minute = t[4]
		
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

	now = Datetime()
	now.now(use_ntp=True)

	print("According to NTP:")
	print(f"time is now: {now.date()}")
	now.replace(hour=now.hour + 1)
	print(f"in an hour its is: {now.date()}")
	print(f"tomorrow is: {now.tomorrow()}")


	# TODO: this implementation does not week since RTC datetime format expects a weekday...
	# Like so: (year, month, day, weekday, hours, minutes, seconds, subseconds)
	# So I need to find a way to determine the weekday based on the timestamp received from NTP
	print("------")
	print("According to RTC:")
	print(f"time is now: {machine.RTC().datetime()}")
