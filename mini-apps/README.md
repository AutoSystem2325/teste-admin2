# OctavioSync - Mini Apps Python

Mini aplicações Python para o sistema OctavioSync.

## 📁 Estrutura

```
mini-apps/
├── shared/           # Módulos compartilhados
├── mae/             # App Mãe (Detecção Visual)
├── filho/           # App Filho (Execução de Comandos)
└── README.md        # Este arquivo
```

## 🚀 Instalação

### Opção 1: Instalação automática (recomendada)
```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh
./install.sh
```

### Opção 2: Instalação manual
```bash
# Dependências básicas
pip install requests python-socketio pyautogui

# Ou use o arquivo simples
pip install -r requirements-simple.txt
```

### Opção 3: Instalação completa
```bash
# Para App Mãe
cd mae
pip install -r requirements.txt

# Para App Filho
cd filho
pip install -r requirements.txt
```

### 2. Configurar servidor
Certifique-se de que o servidor OctavioSync está rodando:
```bash
# No diretório raiz do projeto
npm run start:dev
```

## 📱 Apps Disponíveis

### App Mãe
- **Login/Cadastro** de Mães
- **Detecção visual** de padrões
- **Envio** de comandos via WebSocket

### App Filho
- **Login/Cadastro** de Filhos
- **Recebimento** de comandos via WebSocket
- **Execução** de teclas (F5, F9, F11)

## 🔧 Configuração

Cada app salva o token JWT localmente após o login para autenticação automática.

## 🎯 Uso

1. **Execute o servidor** OctavioSync
2. **Execute o App Mãe** para detectar padrões
3. **Execute o App Filho** para receber comandos
4. **Teste a sincronização** entre Mãe e Filhos
