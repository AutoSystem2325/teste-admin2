# App Filho - OctavioSync

Aplicação Python para recebimento de comandos via WebSocket e execução automática de teclas.

## 🎯 Funcionalidades

- **Login/Cadastro** de Filhos
- **Conexão WebSocket** com o servidor
- **Recebimento de comandos** em tempo real
- **Execução automática** de teclas (F5, F9, F11)
- **Interface gráfica** para monitoramento
- **Log de atividades** em tempo real

## 🚀 Instalação

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar aplicação
```bash
python app_filho.py
```

## 📱 Como usar

### 1. Login/Cadastro
- **Login:** Use email e senha de um Filho existente
- **Cadastrar:** Crie um novo Filho no sistema (precisa do ID da Mãe)

### 2. Conexão
- Após login, a aplicação conecta automaticamente ao WebSocket
- Status de conexão é exibido na interface

### 3. Recebimento de Comandos
- **1C:** Recebe comando → Pressiona F5 automaticamente
- **1V:** Recebe comando → Pressiona F9 automaticamente
- **-:** Recebe comando → Pressiona F11 automaticamente

### 4. Status
- **ON/OFF:** Envie status para o servidor
- **Confirmação:** Recebe confirmação do servidor

### 5. Monitoramento
- Lista de comandos recebidos
- Log mostra todas as atividades
- Execução automática de teclas

## 🔧 Configuração

### Servidor
- **URL:** `http://localhost:3000` (configurável em `shared/config.py`)
- **WebSocket:** `http://localhost:3000`

### Execução de Teclas
As teclas são executadas automaticamente:
```python
if pattern == "1C":
    pyautogui.press('f5')  # Refresh/Reload
elif pattern == "1V":
    pyautogui.press('f9')  # Função específica
elif pattern == "-":
    pyautogui.press('f11') # Fullscreen/Toggle
```

### Segurança
- **FAILSAFE:** Mover mouse para canto superior esquerdo para parar
- **Validação:** Apenas Filhos com validade ativa recebem comandos

## 🐛 Solução de Problemas

### Erro de conexão
- Verifique se o servidor OctavioSync está rodando
- Confirme a URL do servidor em `shared/config.py`

### Erro de autenticação
- Verifique email e senha
- Confirme se o Filho existe no sistema
- Verifique se a licença não expirou

### Teclas não funcionam
- Verifique se `pyautogui` está instalado
- Confirme permissões do sistema
- Teste manualmente: `pyautogui.press('f5')`

### Dependências
- Instale todas as dependências: `pip install -r requirements.txt`
- Python 3.7+ necessário

## ⚠️ Avisos Importantes

### Licença
- Filhos com licença expirada são automaticamente desconectados
- Não recebem comandos quando a validade expira

### Execução de Teclas
- **Cuidado:** As teclas são executadas automaticamente
- **FAILSAFE:** Mova o mouse para o canto superior esquerdo para parar
- **Teste:** Sempre teste em ambiente controlado primeiro

## 📋 Dependências

- `requests` - Cliente HTTP
- `python-socketio` - Cliente WebSocket
- `tkinter` - Interface gráfica
- `pyautogui` - Execução de teclas
- `pynput` - Controle de teclado/mouse



