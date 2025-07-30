import RPi.GPIO as GPIO

from device import Device

GPIO.setmode(GPIO.BCM)


def main():
    try:
        Device().start()
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
