import os
import json
from pathlib import Path

# Caminho absoluto para o banco de dados
caminho_banco = Path(__file__).parents[1] / "banco_dados.db"

CONFIG_PATH = "data/config.json"

# ------------------ CARREGAR CONFIGURAÇÃO ------------------
def carregar_config():
    if not os.path.exists(CONFIG_PATH) or os.stat(CONFIG_PATH).st_size == 0:
        # Cria config padrão com valor_unitario = 1.00
        config = {"valor_unitario": 1.00}
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        return config
    else:
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Se o JSON estiver inválido, recria com valor padrão
            config = {"valor_unitario": 1.00}
            with open(CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=2)
            return config

# ------------------ SALVAR CONFIGURAÇÃO ------------------
def salvar_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
