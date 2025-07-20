import RPi.GPIO as GPIO

from alarmclock import Alarmclock

GPIO.setmode(GPIO.BCM)


def main():
    try:
        Alarmclock().start()
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
