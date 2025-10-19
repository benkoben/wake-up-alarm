from machine import Pin

class ShiftRegister():
    def __init__(self, serial_pin: Pin, clock_pin: Pin, latch_pin: Pin) -> None:
        
        self.serial_pin = Pin(serial_pin, Pin.OUT)
        self.clock_pin = Pin(clock_pin, Pin.OUT)
        self.latch_pin = Pin(latch_pin, Pin.OUT)

    def latch(self):
        self.latch_pin.high()
        self.latch_pin.low()

    def tick(self):
        self.clock_pin.low()
        self.clock_pin.high()
        self.clock_pin.low()

    def write(self, value):
        for i in range(8):
          data = (value >> i) &1
          if data == 0:
            self.serial_pin.low()
          else:
            self.serial_pin.high()
          self.tick()
        self.latch()