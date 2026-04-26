# Wake-up Alarm

A WiFi-connected alarm clock built with a Raspberry Pi Pico 2 W microcontroller.

## Hardware

- **Microcontroller:** Raspberry Pi Pico 2 W
- **Display:** TM1637 4-digit 7-segment display
- **Buzzer:** Piezo buzzer for alarm sound
- **Buttons:** 3x buttons for control

## Features

### Modes

1. **Normal Mode**
   - Displays current time (HH:MM format)
   - **Mode button (press):** Cycle display brightness (3 levels)
   - **Option 1 button:** Show outside temperature (5 seconds)
   - **Option 2 button:** Show inside temperature (5 seconds)
   - **Mode button (hold 2s):** Enter Alarm Adjustment Mode

2. **Alarm Adjustment Mode**
   - **Mode button (press):** Toggle alarm on/off
   - **Mode button (hold 2s):** Exit to Normal Mode
   - **Option 1 button:** Increase time by 1 minute
   - **Option 2 button:** Decrease time by 1 minute
   - Alarm time always scheduled for next occurrence (today if future, tomorrow if past)

3. **Alarm Beeping Mode**
   - Plays "Für Elise" melody until acknowledged
   - **Mode button (press):** Dismiss alarm, schedule for next day
   - **Option 2 button:** Snooze for 9 minutes
   - **Option 1 button:** No action (continues beeping)

## Button Mapping

| Button | Normal Mode | Alarm Adjustment | Alarm Beeping |
|--------|------------|------------------|---------------|
| Mode (press) | Cycle brightness | Toggle alarm on/off | Dismiss alarm |
| Mode (hold) | Enter adj. mode | Exit to normal | - |
| Option 1 | Outside temp | Increase time | No action |
| Option 2 | Inside temp | Decrease time | Snooze 9 min |

## Wiring

```
Pico GP15 → Mode Button → GND
Pico GP14 → Option 1 Button → GND
Pico GP13 → Option 2 Button → GND
Pico GP12 → Buzzer → GND
Pico GP17 → TM1637 CLK
Pico GP16 → TM1637 DIO
```

## Setup

1. Flash MicroPython firmware to Pico 2 W:
   ```bash
   # Enter bootloader mode (hold BOOT, press RESET, release BOOT)
   # Copy UF2 file to Pico (appears as USB drive)
   ```

2. Upload Python files:
   ```bash
   mpremote a0 fs cp *.py :
   mpremote a0 fs cp internal/*.py :internal/
   mpremote a0 fs cp external/*.py :external/
   mpremote a0 fs cp hardware/*.py :hardware/
   ```
3. Install dependencies

```bash
 mpremote mip install datetime
```

4. Configure WiFi in `config.py`:
   ```python
   NetworkConfig.wifi_ssid = "YourSSID"
   NetworkConfig.wifi_key = "YourPassword"
   ```

5. Run:
   ```bash
   mpremote a0 run main.py
   ```

## Project Structure

```
.
├── main.py              # Entry point
├── device.py            # Main control loop
├── alarmclock.py       # Mode state machines
├── config.py           # Configuration
├── wifi.py            # WiFi setup
├── internal/
│   ├── alarm.py       # Alarm state
│   └── notes.py      # Melody notes
├── external/
│   ├── alarm_timestamp.py  # Time handling
│   └── weather_api.py    # Weather API (TODO)
└── hardware/
    ├── button.py        # Button input
    ├── display.py      # TM1637 display
    ├── tm1637.py      # Display driver
    └── wake_up_speaker.py  # Buzzer
```

## Dependencies

- MicroPython v1.28.0+ for Raspberry Pi Pico 2 W
- WiFi network with internet access