from machine import PWM, Pin
import time

class WakeUpSpeaker():
    def __init__(self, pin):
        self.buzzer = PWM(Pin(pin))

    def play_note(self, frequency, duration):
        try:
            print(f"Playing {frequency}Hz for {duration}s")
            """Play a tone at specified frequency for given duration"""
            if frequency > 0:  # Fixed: Changed 'freq' to 'frequency'
                freq = max(20, min(frequency, 20000))
                self.buzzer.freq(int(freq))
                self.buzzer.duty_u16(32768)   # 50% duty cycle
            time.sleep(duration / 1000.0)  # Convert ms to seconds (float division)
            self.buzzer.duty_u16(0)
        except Exception as e:
            print(f"Error playing note: {e}")

    def stop(self):
        self.buzzer.duty_u16(0)

    def play_melody(self, melody):
        """Play a sequence of notes"""
        for freq, dur in melody:
            self.play_note(freq, dur)
            time.sleep(0.05)

if __name__ == "__main__":
    fur_elise = [
        (659.25, 400),  # E5
        (622.25, 400),  # D#5
        (659.25, 400),  # E5
        (622.25, 400),  # D#5
        (659.25, 400),  # E5
        (493.88, 400),  # B4
        (587.33, 400),  # D5
        (523.25, 400),  # C5
        (440.00, 800),  # A4

        (0, 300),       # rest
        (349.23, 400),  # F4
        (440.00, 400),  # A4
        (493.88, 600),  # B4

        (392.00, 400),  # G4
        (0, 100),       # rest
        (659.25, 400),  # E5
        (622.25, 400),  # D#5
        (659.25, 400),  # E5
        (622.25, 400),  # D#5
        (659.25, 400),  # E5
        (493.88, 400),  # B4
        (587.33, 400),  # D5
        (523.25, 400),  # C5
        (440.00, 800),  # A4

        (349.23, 400),  # F4
        (440.00, 400),  # A4
        (493.88, 600),  # B4
        (0, 300),       # rest

        (523.25, 400),  # C5
        (493.88, 400),  # B4
        (440.00, 800),  # A4
    ]

    buzzer = WakeUpSpeaker(12)
    print("Playing Für Elise...")
    buzzer.play_melody(fur_elise)
    print("Done!")
