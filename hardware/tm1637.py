from machine import Pin
import time

# Constants
TM1637_I2C_COMM1 = 0x40
TM1637_I2C_COMM2 = 0xC0
TM1637_I2C_COMM3 = 0x80
COLON_BIT = 0x40 # Some modules use 0x80 for colon instead

# Digit to segment map
digitToSegment = [
    0b00111111,  # 0
    0b00000110,  # 1
    0b01011011,  # 2
    0b01001111,  # 3
    0b01100110,  # 4
    0b01101101,  # 5
    0b01111101,  # 6
    0b00000111,  # 7
    0b01111111,  # 8
    0b01101111,  # 9
    0b01110111,  # A
    0b01111100,  # b
    0b00111001,  # C
    0b01011110,  # d
    0b01111001,  # E
    0b01110001   # F
]

minusSegments = 0b01000000

class TM1637Display:
    def __init__(self, pinClk, pinDIO, bitDelay=100):
        self.clk = Pin(pinClk, Pin.OPEN_DRAIN)
        self.dio = Pin(pinDIO, Pin.OPEN_DRAIN)
        self.bitDelay = bitDelay
        self.brightness = 0x0f

        # Release both lines (HIGH via pull-up)
        self.clk.value(1)
        self.dio.value(1)

    # -------------------------
    # Basic control
    # -------------------------
    def _bit_delay(self):
        time.sleep_us(self.bitDelay)

    def _start(self):
        self.dio.value(1)
        self.clk.value(1)
        self._bit_delay()
        self.dio.value(0)

    def _stop(self):
        self.clk.value(0)
        self._bit_delay()
        self.dio.value(0)
        self._bit_delay()
        self.clk.value(1)
        self._bit_delay()
        self.dio.value(1)

    def _write_byte(self, b):
        data = b

        for i in range(8):
            self.clk.value(0)
            self._bit_delay()

            self.dio.value(data & 0x01)

            self._bit_delay()
            self.clk.value(1)
            self._bit_delay()

            data >>= 1

        # ACK
        self.clk.value(0)
        self.dio.value(1)  # release
        self._bit_delay()

        self.clk.value(1)
        self._bit_delay()

        ack = self.dio.value()

        self.clk.value(0)
        self._bit_delay()

        return ack

    # -------------------------
    # Public API
    # -------------------------
    def setBrightness(self, brightness, on=True):
        self.brightness = (brightness & 0x07) | (0x08 if on else 0x00)

    def setSegments(self, segments, length=4, pos=0):
        # COMM1
        self._start()
        self._write_byte(TM1637_I2C_COMM1)
        self._stop()

        # COMM2
        self._start()
        self._write_byte(TM1637_I2C_COMM2 + (pos & 0x03))

        for i in range(length):
            self._write_byte(segments[i])

        self._stop()

        # COMM3
        self._start()
        self._write_byte(TM1637_I2C_COMM3 + (self.brightness & 0x0f))
        self._stop()

    def clear(self):
        self.setSegments([0, 0, 0, 0])

    # -------------------------
    # Number display
    # -------------------------
    def encodeDigit(self, digit):
        return digitToSegment[digit & 0x0F]

    def showDots(self, dots, digits):
        for i in range(4):
            digits[i] |= (dots & 0x80)
            dots <<= 1

    def showNumberDec(self, num, leading_zero=True, colon=True, length=4, pos=0):
        self.showNumberBaseEx(-10 if num < 0 else 10,
                             -num if num < 0 else num,
                             COLON_BIT if colon else 0, leading_zero, length, pos)

    def showNumberBaseEx(self, base, num, dots, leading_zero, length, pos):
        negative = False
        if base < 0:
            base = -base
            negative = True

        digits = [0] * 4

        if num == 0 and not leading_zero:
            for i in range(length - 1):
                digits[i] = 0
            digits[length - 1] = self.encodeDigit(0)
        else:
            for i in range(length - 1, -1, -1):
                digit = num % base

                if digit == 0 and num == 0 and not leading_zero:
                    digits[i] = 0
                else:
                    digits[i] = self.encodeDigit(digit)

                if digit == 0 and num == 0 and negative:
                    digits[i] = minusSegments
                    negative = False

                num //= base

        if dots != 0:
            self.showDots(dots, digits)

        self.setSegments(digits, length, pos)

if __name__ == "__main__":
    display = TM1637Display(17, 16)
    display.setBrightness(0)
    display.showNumberDec(1337)
    time.sleep(1)
    display.clear()
