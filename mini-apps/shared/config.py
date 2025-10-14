"""
Configurações compartilhadas para os mini apps
"""
import os
from pathlib import Path

# Configurações do servidor
SERVER_URL = "http://localhost:3000"
WEBSOCKET_URL = "http://localhost:3000"

# Caminhos dos arquivos de configuração
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
TOKEN_FILE_MAE = CONFIG_DIR / "mae_token.txt"
TOKEN_FILE_FILHO = CONFIG_DIR / "filho_token.txt"

# Criar diretório de configuração se não existir
CONFIG_DIR.mkdir(exist_ok=True)

# Configurações de detecção visual - SIMPLIFICADO PARA FUNCIONAR
DETECTION_CONFIG = {
    "pattern_1c": {
        "name": "1C",
        "description": "Padrão 1C - Amarelo/Dourado",
        "color_min_rgb": (100, 80, 0),     # Range MUITO amplo para pegar qualquer amarelo
        "color_max_rgb": (255, 255, 150),  # Inclui todos os tons amarelos possíveis
        "threshold_pct": 1.0,              # ULTRA sensível - apenas 1%
        "key": "F5"
    },
    "pattern_1v": {
        "name": "-1V", 
        "description": "Padrão -1V - Verde",
        "color_min_rgb": (0, 80, 0),       # Range MUITO amplo para pegar qualquer verde
        "color_max_rgb": (150, 255, 150),  # Inclui todos os tons verdes possíveis
        "threshold_pct": 1.0,              # ULTRA sensível - apenas 1%
        "key": "F6"
    },
    "pattern_neutral": {
        "name": "-",
        "description": "Padrão Neutro - Qualquer coisa que não seja verde ou amarelo",
        "color_min_rgb": (0, 0, 0),        # Preto
        "color_max_rgb": (120, 120, 120),  # Cinza
        "threshold_pct": 30.0,             # 30% da área
        "key": "F11"
    }
}

# Configurações de interface
UI_CONFIG = {
    "window_title": "OctavioSync",
    "window_size": "400x300",
    "font_family": "Arial",
    "font_size": 10
}


