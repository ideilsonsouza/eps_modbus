import json
import os

# Arquivo de configuração
CONFIG_FILE = "config.json"


def load_config():
    """
    Carrega o arquivo JSON de configuração ou cria um padrão.
    """
    if CONFIG_FILE in os.listdir():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        # Configuração inicial padrão
        config = {
            "registers": [
                {"address": 0, "value": 12345, "format": "int"},
                {"address": 1, "value": 6789, "format": "int"}
            ]
        }
        save_config(config)
        return config


def save_config(config):
    """
    Salva as configurações no arquivo JSON.
    """
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def add_register(config, address, value, data_format):
    """
    Adiciona um novo registrador.
    """
    config["registers"].append({"address": address, "value": value, "format": data_format})
    save_config(config)
    

def set_register_value(config, address, value):
    """
    Atualiza o valor de um registrador pelo endereço.
    """
    for reg in config["registers"]:
        if reg["address"] == address:
            reg["value"] = value
            save_config(config)
            return True
    return False

def get_register_value(config, address):
    """
    Retorna o valor de um registrador pelo endereço.
    """
    for reg in config["registers"]:
        if reg["address"] == address:
            return reg["value"]
    return None