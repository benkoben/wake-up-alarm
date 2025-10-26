
from machine import Pin
import time

dataPin = Pin(15, Pin.OUT)
clockPin = Pin(13, Pin.OUT)
latchPin = Pin(14, Pin.OUT)

dp1=Pin(16, Pin.OUT)
dp2=Pin(17, Pin.OUT)
dp3=Pin(18, Pin.OUT)
dp4=Pin(19, Pin.OUT)

common_cathodes = [dp1, dp2, dp3, dp4]

one = 0b00010100
two = 0b11101100
three = 0b10111100
four = 0b00011110
five = 0b10111010
six = 0b11111010
seven = 0b10010100

numbers = {
    "1": one,
    "2": two,
    "3": three,
    "4": four,
    "5": five,
    "6": six,
    "7": seven
}

target = "1337"

def latch():
  latchPin.high()
  latchPin.low()

def tick():
  clockPin.low()
  clockPin.high()
  clockPin.low()

def write(value):
  for i in range(8):
    print(i, " = ", ((value >> i ) &1))
    data = (value >> i) &1
    if data == 0:
      dataPin.high()
    else:
      dataPin.low()
    tick()
  latch()


def main():
    while True:
        for i, num in enumerate(target):

            # turn off displays
            for cc in common_cathodes:
               cc.low()

            value = numbers[num]
            write(value)
            # only light one display
            common_cathodes[i].high()

        for cc in common_cathodes:
           # turn off displays
           cc.low()

if __name__ == "__main__":
   main()