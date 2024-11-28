
from machine import reset
from data import  add_register


def web_page(config):
    """
    Gera página HTML para configuração.
    """
    registers_table = "".join(
        f"<tr><td>{reg['address']}</td><td>{reg['value']}</td><td>{reg['format']}</td></tr>"
        for reg in config["registers"]
    )
    return f"""
    <html>
    <head>
        <title>Settings</title>
    </head>
    <body>
        <h1>Registers</h1>
        <table border="1">
            <tr><th>Address</th><th>Value</th><th>Format</th></tr>
            {registers_table}
        </table>
        <form method="POST" action="/">
            <input name="address" placeholder="Address">
            <input name="value" placeholder="Value">
            <input name="format" placeholder="Format">
            <button>Add</button>
        </form>
        <br>
        <form method="POST" action="/reset">
            <button>Reboot ESP32</button>
        </form>
    </body>
    </html>
   """


def start_web_server(server_socket, config):
    """
    Processa requisições HTTP.
    """
    try:
        client_socket, _ = server_socket.accept()
        request = client_socket.recv(1024).decode()
        if "POST" in request:
            if "/reset" in request:
                reset()  # Reinicia o ESP32
            else:
                body_start = request.find("\r\n\r\n") + 4
                params = dict(p.split("=") for p in request[body_start:].split("&"))
                add_register(config, int(params["address"]), int(params["value"]), params["format"])
        response = web_page(config)
        client_socket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
        client_socket.close()
    except Exception as e:
        print("Erro no servidor Web:", e)
