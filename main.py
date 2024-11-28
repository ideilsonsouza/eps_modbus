import socket
import select
from data import load_config
from web import start_web_server
from modbus import start_modbus_server
from boot import WIFI_IP

def main():
    config = load_config()

    # Criação dos sockets para Modbus e Web
    modbus_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    modbus_socket.bind(("0.0.0.0", 502))
    modbus_socket.listen(1)

    web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    web_socket.bind(("0.0.0.0", 80))
    web_socket.listen(1)

    print(f"Servidores iniciados. Acesse http://{WIFI_IP} para configuração.")

    # Usando select para monitorar múltiplos sockets
    while True:
        # Espera por atividades em qualquer um dos sockets
        readable, _, _ = select.select([modbus_socket, web_socket], [], [])

        for sock in readable:
            if sock is modbus_socket:
                # Lida com novas conexões Modbus
                start_modbus_server(sock, config)
            elif sock is web_socket:
                # Lida com novas conexões Web
                start_web_server(sock, config)

if __name__ == "__main__":
    main()
