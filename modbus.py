import struct
import time
from data import get_register_value, set_register_value


def handle_modbus_request(request, config):
    """
    Trata requisições Modbus.
    """
    if len(request) < 8:
        return b""

    transaction_id = request[:2]
    protocol_id = request[2:4]
    unit_id = request[6]
    function_code = request[7]

    # Função 3: Read Holding Registers
    if function_code == 3:
        start_address = struct.unpack(">H", request[8:10])[0]
        register_count = struct.unpack(">H", request[10:12])[0]

        response_data = b""
        for i in range(register_count):
            value = get_register_value(config, start_address + i)
            if value is None:
                return (
                    transaction_id +
                    protocol_id +
                    struct.pack(">H", 3) +
                    bytes([unit_id, 0x83, 2])  # Endereço inválido
                )
            response_data += struct.pack(">H", value)

        return (
            transaction_id +
            protocol_id +
            struct.pack(">H", 3 + len(response_data)) +
            bytes([unit_id, function_code]) +
            bytes([len(response_data)]) +
            response_data
        )

    # Função 6: Write Single Register
    elif function_code == 6:
        address = struct.unpack(">H", request[8:10])[0]
        value = struct.unpack(">H", request[10:12])[0]
        if not set_register_value(config, address, value):
            return (
                transaction_id +
                protocol_id +
                struct.pack(">H", 3) +
                bytes([unit_id, 0x86, 2])  # Endereço inválido
            )
        return request

    return b""

def start_modbus_server(server_socket, config):
    """
    Processa requisições Modbus TCP.
    """
    try:
        client_socket, _ = server_socket.accept()
        request = client_socket.recv(1024)
        if request:
            response = handle_modbus_request(request, config)
            client_socket.send(response)
        client_socket.close()
    except Exception as e:
        print("Erro no servidor Modbus:", e)