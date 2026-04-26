import network
import time
import usocket as socket

from machine import Pin
from config import NetworkConfig

ONBOARD_LED = Pin('LED', Pin.OUT, value=0)

network_statuses = {
    network.STAT_CONNECT_FAIL: "CONNECT_FAIL", 
    network.STAT_IDLE: "IDLE", 
    network.STAT_WRONG_PASSWORD: "WRONG_PASSWORD", 
    network.STAT_NO_AP_FOUND: "NO_AP_FOUND", 
    network.STAT_CONNECTING: "CONNECTING", 
}
    
def set_wifi(ssid: str, key: str):
    nic = network.WLAN(network.STA_IF)
    if nic.isconnected():
        print(f"Connected to SSID {NetworkConfig.wifi_ssid}, ifconfig: {nic.ifconfig()}")
        return

    nic.active(True)
    nic.connect(
        ssid, key
    ) 

    # Wait and poll for 15 seconds
    for i in range(30):
        # slow blink to show that WIFI connection is in progress
        ONBOARD_LED.toggle()
        # keep LED static for 3 seconds and then turn off to indicate success
        if nic.status() == network.STAT_GOT_IP:
            ONBOARD_LED.high()
            time.sleep(3)
            ONBOARD_LED.low()
            return
        time.sleep(0.5)

    print(f"Wifi status: {network_statuses[nic.status()]}")
    if nic.status() == network.STAT_CONNECT_FAIL or nic.status() == network.STAT_WRONG_PASSWORD:
        # If there was no connection after 15 seconds 
        # blink rapidly to indicate connection failure
        for i in range(100):
            time.sleep(0.1)
            ONBOARD_LED.toggle()
    ONBOARD_LED.low()


if __name__ == "__main__":
    set_wifi(
        ssid = NetworkConfig.wifi_ssid,
        key = NetworkConfig.wifi_key,
    )
