import network


def connect_router(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def setup_ap(ssid, password):
    ap_if = network.WLAN(network.AP_IF)
    if not ap_if.active():
        print('establishing AP')
        ap_if.active(True)
        ap_if.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)  # 设置接入点
    print('AP config:', ap_if.ifconfig())
