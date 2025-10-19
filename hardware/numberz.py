class Number():
    def __init__(self, num: int) -> None:
        _schema = {
            2: 0b00101000,
            1: 0b10110011,
            3: 0b10111010,
            4: 0b01111000,
            5: 0b11011010,
            6: 0b10101000,
            7: 0b11011011,
            8: 0b11111111,
            9: 0b11111010,
            0: 0b11101011,
            # TODO add the remaining numbers
        }
        self._key = num
        self.value = _schema[num]

    def __repr__(self) -> int:
        return f"{self._key} = {self.value}"

    def enable_dot(self):
        if self.value & 1 == 0:
            self.value += 1

    def disable_dot(self):
        if self.value & 1 == 1:
            self.value -= 1

