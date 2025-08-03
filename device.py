import time
import alarmclock
import RPi.GPIO as GPIO

from datetime import datetime
from internal import alarm


class Device():
    def __init__(self): 
        self.alarmclock = alarmclock.NormalMode(
            alarm.Alarm()
        )

    def shutdown(self):
        print("Shutting down...")
        print("Cleaning up resources...")
        self.alarmclock.cleanup()

    # start runs the alarm clock's main control loop
    def start(self):
        while True:
            
            alarm_time_passed = self.alarmclock.current_time > self.alarmclock.alarm.timestamp
            alarm_active = self.alarmclock.alarm.is_active
            active_mode = self.alarmclock.__repr__()
            in_normal_mode = active_mode == "NormalMode"

            # If the alarm is active and has been surpassed
            # and the device is operating in NormalMode,
            # then we need to trigger a sound
            # and start blinking the display.
            if alarm_active and alarm_time_passed and in_normal_mode:
                print(f"{self.alarmclock.current_time} > {self.alarmclock.alarm.timestamp} ?")
                # Switch from NormalMode to AlarmBeepingMode
                self.alarmclock = self.alarmclock.mode_button_event('alarm_trigger')
                # This will run a sequence where the buzzer is active until the alarm has been acknowledged.
                # running...
                # running...
                # running...
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
                        time.sleep(1)
                        hold_event = True

                if not hold_event: # its a press event
                    self.alarmclock.mode_button_event('press'),

            # Middle button (+ / weather)
            if self.alarmclock.option1_button.is_high():
                self.alarmclock.aux1_button_event(None)

            # Right button ( - / inside temp )
            if self.alarmclock.option2_button.is_high():
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
