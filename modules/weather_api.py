import os
import requests
import json

from datetime import datetime


class WeatherApiClient():
    def __init__(self, key):
        self.key = key


class Location(WeatherApiClient):
    def __init__(self, key, lat, lon):
        super().__init__(key)

        self.lon = lon
        self.lat = lat
        self.temperature = None
        self.ttl = 30  # minutes
        self.last_updated = datetime.now()  # datetime
        self._set_url()

    def _set_url(self):

        self.url = "".join([
            "https://api.openweathermap.org/data/2.5/weather",
            f"?lat={self.lat}",
            f"&lon={self.lon}",
            f"&appid={self.key}",
            "&units=metric"
        ])

        print(self.url)

    def _set_temperature(self, temp: float) -> str:
        value = f"{temp}".split(".")[0]
        self.temperature = value.rjust(4, " ")
        self.last_updated = datetime.now()

    # retrieve weather data for a location. If TTL has not yet been reached then self.temperature is returned
    def get_weather(self):
        if (datetime.now() - self.last_updated).seconds > self.ttl * 60 or self.temperature is None:
            print("cache miss")
            response = requests.get(self.url)
            forecast = json.loads(response.text)
            self._set_temperature(forecast["main"]["temp"])

        return self.temperature
