from machine import Pin
import time

displayPin = Pin(16, Pin.OUT).value(1)
dataPin = Pin(15, Pin.OUT)
clockPin = Pin(13, Pin.OUT)
latchPin = Pin(14, Pin.OUT)

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

  one = 0b00100100 
  two = 0b01101011
  three = 0b01101110
  four = 0b00111100
  five = 0b01011110

  while True:
    for number in [one, two]:
      write(number)
      time.sleep(0.3)


if __name__ == "__main__":
   main()