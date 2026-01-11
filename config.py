class Config():
    button_1_pin: int = 4
    button_2_pin: int = 2
    button_3_pin: int = 7

    # Sound
    buzzer_pin: int = 21

    digit_pins: list = [20, 27, 13, 10]  # GPIO pins
    clock_pin = 14
    latch_pin = 5
    serial_pin = 18
    colon_switch_pin = 28
    colon_pwr_pin = 16

class WeatherConfig():
    # authentication keys
    weather_api_key = ""
    # locatio60
    latitude = 55.6
    longitude = 13.00

class NetworkConfig():
    wifi_ssid = "JunoBanuno"
    wifi_key = "Kooijsson9598"
    ntp_server = "pool.ntp.org"
