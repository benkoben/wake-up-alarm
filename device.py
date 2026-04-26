import time
import alarmclock
import wifi

import internal.alarm as alarm

from datetime import datetime
from machine import Pin, RTC
from config import NetworkConfig, Config
from external import alarm_timestamp

import hardware.button as button

class Device():
    def __init__(self): 
        self.alarmclock = alarmclock.NormalMode(
            alarm.Alarm()
        )

        wifi.set_wifi(NetworkConfig.wifi_ssid, NetworkConfig.wifi_key)
        print("connected to wifi")
        print("ready to start")

        rtc = RTC()
        now = alarm_timestamp.Ntp(NetworkConfig.ntp_server)
        rtc.datetime((
            now.year(),
            now.month(),
            now.monthday(),
            now.weekday(),
            now.hour(),
            now.minute(),
            now.second(),
            0
        ))
        print("RTC timestamp: ", rtc.datetime())


    def shutdown(self):
        print("Shutting down...")
        print("Cleaning up resources...")
        self.alarmclock.cleanup()

    # start runs the alarm clock's main control loop
    def start(self):
        
        try:
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
                if self.alarmclock.mode_button.is_pressed():
                    delta = datetime.now()
                    while self.alarmclock.mode_button.is_pressed():
                        time.sleep(0.1)
                        if (datetime.now() - delta).seconds >= 2:
                            # switch state
                            self.alarmclock = self.alarmclock.mode_button_event('hold')
                            time.sleep(1)
                            hold_event = True

                    if not hold_event: # its a press event
                        self.alarmclock.mode_button_event('press')

                # Middle button (+ / weather)
                if self.alarmclock.option1_button.is_pressed():
                    self.alarmclock.aux1_button_event(None)

                # Right button ( - / inside temp )
                if self.alarmclock.option2_button.is_pressed():
                    self.alarmclock.aux2_button_event(None)

                # Sets the content on the 7 Segment 4 Digit display
                # Render different things depending on the active mode
                self.alarmclock.refresh_display()
        except Exception as e:
            print(f"exception occured: {e}")
            self.shutdown()
