from dataclasses import dataclass
from dotenv import load_dotenv

import os

load_dotenv()

@dataclass()
class Config():
    button_1_pin: int = 15
    button_2_pin: int = 26
    button_3_pin: int = 16

    # 7 seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
    segment_pins: tuple = (11, 4, 23, 8, 7, 10, 18, 25)  # GPIO pins
    digit_pins: tuple = (22, 27, 17, 24)  # GPIO pins

@dataclass()
class WeatherConfig():
    # authentication keys
    weather_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    # locatio60
    latitude = 55.6
    longitude = 13.00

