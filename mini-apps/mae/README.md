# App Mãe - OctavioSync

Aplicação Python para detecção visual de padrões e envio de comandos via WebSocket.

## 🎯 Funcionalidades

- **Login/Cadastro** de Mães
- **Conexão WebSocket** com o servidor
- **Envio de padrões** (1C, 1V, -)
- **Interface gráfica** simples e intuitiva
- **Log de atividades** em tempo real

## 🚀 Instalação

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar aplicação
```bash
python app_mae.py
```

## 📱 Como usar

### 1. Login/Cadastro
- **Login:** Use email e senha de uma Mãe existente
- **Cadastrar:** Crie uma nova Mãe no sistema

### 2. Conexão
- Após login, a aplicação conecta automaticamente ao WebSocket
- Status de conexão é exibido na interface

### 3. Envio de Padrões
- **1C:** Envia comando para pressionar F5
- **1V:** Envia comando para pressionar F9
- **-:** Envia comando para pressionar F11

### 4. Monitoramento
- Log mostra todas as atividades
- Confirmação de envio de comandos

## 🔧 Configuração

### Servidor
- **URL:** `http://localhost:3000` (configurável em `shared/config.py`)
- **WebSocket:** `http://localhost:3000`

### Padrões
Os padrões são configurados em `shared/config.py`:
```python
DETECTION_CONFIG = {
    "pattern_1c": {"name": "1C", "key": "F5"},
    "pattern_1v": {"name": "1V", "key": "F9"},
    "pattern_neutral": {"name": "-", "key": "F11"}
}
```

## 🐛 Solução de Problemas

### Erro de conexão
- Verifique se o servidor OctavioSync está rodando
- Confirme a URL do servidor em `shared/config.py`

### Erro de autenticação
- Verifique email e senha
- Confirme se a Mãe existe no sistema

### Dependências
- Instale todas as dependências: `pip install -r requirements.txt`
- Python 3.7+ necessário

## 📋 Dependências

- `requests` - Cliente HTTP
- `python-socketio` - Cliente WebSocket
- `tkinter` - Interface gráfica
- `Pillow` - Processamento de imagem
- `opencv-python` - Detecção visual
- `numpy` - Computação numérica
- `pyautogui` - Automação de interface



