import network
import time

# Configurações Wi-Fi
WIFI_SSID = "workspace"
WIFI_PASSWORD = "@Ics#2304"

WIFI_IP = None

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Conectando ao Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Conectado! IP:", wlan.ifconfig()[0])
    
    return wlan.ifconfig()[0]

try:
    WIFI_IP = connect_wifi(WIFI_SSID, WIFI_PASSWORD)
except Exception as e:
    print("Erro ao conectar ao Wi-Fi:", e)

