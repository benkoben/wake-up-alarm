import time
import alarmclock
import RPi.GPIO as GPIO

from datetime import datetime
from internal import alarm


class Device():
    def __init__(self):
        self.alarmclock = alarmclock.NormalMode(alarm.Alarm())

    def shutdown(self):
        print("Shutting down...")
        print("Cleaning up resources...")
        self.alarmclock.cleanup()

    # start runs the alarm clock's main control loop
    def start(self):
        while True:

            # TODO: This logic does not work correctly
            if datetime.now() > self.alarmclock.alarm_time and self.alarmclock.alarm.is_active:
                # If the alarm is active and has been surpassed then we need to trigger a sound
                # and start blinking the display.

                # Switch from NormalMode to AlarmBeepingMode
                self.alarmclock = self.alarmclock.mode_button_event('alarm_trigger')
                print(f"now in {self.alarmclock} mode")

                # Switch from AlarmBeepingMode to NormalMode (if the alarm is acknowledged)
                self.alarmclock = self.alarmclock.mode_button_event('alarm_trigger')

            # Detect what type of button press
            # If the user holds the button for 1 second a 'hold' event is registered
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
                print("middle button pressed")
                self.alarmclock.aux1_button_event(None)

            # Right button ( - / inside temp )
            if self.alarmclock.aux2_button.is_high():
                print("right button pressed")
                self.alarmclock.aux2_button_event(None)

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
