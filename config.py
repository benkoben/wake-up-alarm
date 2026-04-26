class Config():
    button_1_pin: int = 15
    button_2_pin: int = 14
    button_3_pin: int = 13

    # Sound
    buzzer_pin: int = 12
    
    # TM1367
    clock_pin = 17
    dio_pin = 16

class WeatherConfig():
    # authentication keys
    weather_api_key = ""
    # locatio60
    latitude = 55.6
    longitude = 13.00

class NetworkConfig():
    wifi_ssid = "JunoBabuno"
    wifi_key = "Kooijsson9598"
    ntp_server = "pool.ntp.org"
