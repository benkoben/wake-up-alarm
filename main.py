from device import Device

def main():
    device = Device()

    try:
        device.start()
    finally:
        device.shutdown()


if __name__ == "__main__":
    main()
