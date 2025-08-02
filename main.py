import RPi.GPIO as GPIO

from device import Device

GPIO.setmode(GPIO.BCM)


def main():
    device = Device()

    try:
        device.start()
    finally:
        GPIO.cleanup()
        device.shutdown()


if __name__ == "__main__":
    main()
