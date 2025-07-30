import time
import alarmclock
import RPi.GPIO as GPIO

from datetime import datetime
from internal import alarm

class Device():
    def __init__(self):
        self.alarmclock = alarmclock.NormalMode(alarm.Alarm())

    # start runs the alarm clock's main control loop
    def start(self):
        while True:

            hold_event = False
            # Mode button
            if self.alarmclock.mode_button.is_high():
                count = datetime.now()
                while self.alarmclock.mode_button.is_high():
                    if (datetime.now() - count).seconds >= 1:
                        # switch state
                        self.alarmclock = self.alarmclock.mode_button_event('hold')
                        print(f"switched mode to {self.alarmclock}")
                        time.sleep(1)
                        hold_event = True

                if not hold_event: # its a press event
                    self.alarmclock.mode_button_event('press'),

            # Middle button (+ / weather)
            if self.alarmclock.aux1_button.is_high():
                self.alarmclock.aux1_event(None)
                continue

            # Right button ( - / inside temp )
            if self.alarmclock.aux2_button.is_high():
                self.alarmclock.aux2_event(None)
                continue

            # Sets the content on the 7 Segment 4 Digit display
            # Render different things depending on mode
            self.alarmclock.refresh_display()


if __name__ == "__main__":
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    a = alarmclock.Alarmclock()
    try:
        while True:
            a._display.update_content(" 0FF")
            a._display.render()
    finally:
        GPIO.cleanup()
