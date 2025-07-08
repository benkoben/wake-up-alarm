# code modified, tweaked and tailored from code by bertwert
# on RPi forum thread topic 91796
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# GPIO ports for the 7seg pins
segments = (11, 4, 23, 8, 7, 10, 18, 25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# GPIO ports for the digit 0-3 pins
# digits = (22,)
digits = (22, 27, 17, 24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (0, 0, 0, 0, 0, 0, 1),
       '1': (1, 0, 0, 1, 1, 1, 1),
       '2': (0, 0, 1, 0, 0, 1, 0),
       '3': (0, 0, 0, 0, 1, 1, 0),
       '4': (1, 0, 0, 1, 1, 0, 0),
       '5': (0, 1, 0, 0, 1, 0, 0),
       '6': (0, 1, 0, 0, 0, 0, 0),
       '7': (0, 0, 0, 1, 1, 1, 1),
       '8': (0, 0, 0, 0, 0, 0, 0),
       '9': (0, 0, 0, 0, 1, 0, 0)}

def run_clock():
    while True:
        s = time.ctime()[11:13] + time.ctime()[14:16]
        for digit in range(0, 4):
            other_displays = digits[:digit] + digits[digit+1:]
            for other_display in other_displays:
                GPIO.output(other_display, 0)

            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
                GPIO.output(25, 1)

            time.sleep(0.002)
            for other_display in other_displays:
                GPIO.output(other_display, 1)




try:
   run_clock()
finally:
    GPIO.cleanup()