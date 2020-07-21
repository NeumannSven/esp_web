import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    wlan.connect('YOUR_SSID','YOUR_WIFI_PASSWORD')
    while not wlan.isconnected():
        pass
    print("Netzwerkkonfiguration: ", wlan.ifconfig())
    