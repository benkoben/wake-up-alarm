# wake-up-alarm

Welcome to my summer project 2025. I used to project to learn more about DIY electronics and microcontrollers.
It is a small WIFI connected wake up alarm.

# Bit mapping

> The least significant bit is used to control the dots on each digit. All other bits are mapped to a specific segment of the display.

Here are the mappings between shift register and 7 segent 4 digit display:

||||||||||Decimal|
|-|-|-|-|-|-|-|-|-|-|
|Bit|128|64|32|16|8|4|2|1||
|Shift register|Qa|Qb|Qc|Qd|Qe|Qf|Qg|Qh|
|Display|A|F|B|G|C|DP|D|E|
|1|0|0|1|0|1|0|0|0||
|2|1|0|1|1|0|0|1|1||
|3|1|0|1|1|1|0|1|0||
|4|0|1|1|1|1|0|0|0||
|5|1|1|0|1|1|0|1|0||
|6|1|1|0|1|1|0|1|1||
|7|1|0|1|0|1|0|0|0||
|8|1|1|1|1|1|0|1|1||
|9|1|1|1|1|1|0|1|0||
|0|1|1|1|0|1|0|1|1||

# TODO/Features

- [ ] Add snooze
- [ ] Add a temp/humid sensor
