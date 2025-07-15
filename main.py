import RPi.GPIO as GPIO
import time

from internal import display

GPIO.setmode(GPIO.BCM)

SEGMENTS = (11, 4, 23, 8, 7, 10, 18, 25)
DIGITS = (22, 27, 17, 24)

def main():
    try:
        module = display.Display(
            refresh_rate=0.005,
            segment_pins=SEGMENTS,
            digit_pins=DIGITS
        )

        while True:
            # Retrieve time
            s = time.ctime()[11:13] + time.ctime()[14:16]

            # Render time on module 7 Segment 4 Digit display
            module.render(s)

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
