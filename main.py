import json
import os
import socket
import struct
import time
from data import load_config
from web import start_web_server
from modbus import start_modbus_server
from boot import WIFI_IP

def main():
    config = load_config()

    modbus_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    modbus_socket.bind(("0.0.0.0", 502))
    modbus_socket.listen(1)

    web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    web_socket.bind(("0.0.0.0", 80))
    web_socket.listen(1)

    print(f"Servidores iniciados. Acesse http://{WIFI_IP}> para configuração.")
    while True:
        start_modbus_server(modbus_socket, config)
        start_web_server(web_socket, config)

if __name__ == "__main__":
    main()
