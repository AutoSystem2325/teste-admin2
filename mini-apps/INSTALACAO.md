# Guia de Instalação - Mini Apps OctavioSync

## 📋 Pré-requisitos

- **Python 3.7+** instalado
- **Servidor OctavioSync** rodando
- **PostgreSQL** configurado

## 🚀 Instalação Rápida

### 1. Clonar/Download do projeto
```bash
# Se usando git
git clone <repo-url>
cd octavio-sync-api

# Ou baixe e extraia o projeto
```

### 2. Instalar dependências do servidor
```bash
# No diretório raiz
npm install
npm run start:dev
```

### 3. Instalar dependências dos mini apps

#### Opção 1: Instalação simples (recomendada)
```bash
cd mini-apps
pip install -r requirements-simple.txt
```

#### Opção 2: Instalação completa
```bash
# App Mãe
cd mini-apps/mae
pip install -r requirements.txt

# App Filho
cd mini-apps/filho
pip install -r requirements.txt
```

#### Opção 3: Instalação manual
```bash
pip install requests python-socketio pyautogui
```

## 🎯 Execução

### 1. Iniciar servidor
```bash
# No diretório raiz
npm run start:dev
```

### 2. Executar App Mãe
```bash
cd mini-apps/mae
python app_mae.py
```

### 3. Executar App Filho
```bash
cd mini-apps/filho
python app_filho.py
```

## 🔧 Configuração

### URLs do Servidor
Edite `mini-apps/shared/config.py` se necessário:
```python
SERVER_URL = "http://localhost:3000"
WEBSOCKET_URL = "http://localhost:3000"
```

### Banco de Dados
Configure o arquivo `.env` no diretório raiz:
```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/octavio_sync?schema=public"
JWT_SECRET="your-secret-key"
```

## 🧪 Teste Completo

### 1. Criar dados de teste
```bash
# No diretório raiz
npm run prisma:seed
```

### 2. Testar fluxo completo
1. **Execute o servidor** OctavioSync
2. **Execute o App Mãe** e faça login
3. **Execute o App Filho** e faça login
4. **Envie padrão** no App Mãe
5. **Verifique execução** no App Filho

## 🐛 Solução de Problemas

### Erro de dependências Python (Windows)
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências básicas primeiro
pip install requests
pip install python-socketio
pip install pyautogui

# Se der erro com Pillow, pule por enquanto
# pip install Pillow
```

### Erro de compilação (Windows)
```bash
# Instalar Visual Studio Build Tools
# Ou usar versões pré-compiladas
pip install --only-binary=all requests python-socketio pyautogui
```

### Erro de permissões
```bash
# No Windows, execute como administrador
# Ou use --user
pip install --user requests python-socketio pyautogui
```

### Erro de conexão WebSocket
- Verifique se o servidor está rodando
- Confirme a URL em `shared/config.py`
- Verifique firewall/antivírus

### Erro de execução de teclas
```bash
# No Linux, pode precisar de permissões
sudo apt-get install python3-tk

# No Windows, execute como administrador se necessário
```

### Erro de banco de dados
```bash
# Executar migrações
npx prisma migrate dev

# Verificar conexão
npx prisma studio
```

## 📱 Dados de Teste

Após executar o seed:
- **Mãe:** `mae@exemplo.com` / `123456`
- **Filho:** `filho1@exemplo.com` / `123456`

## 🎉 Pronto!

Agora você tem o sistema completo funcionando:
- ✅ **Servidor** OctavioSync rodando
- ✅ **App Mãe** para detectar e enviar padrões
- ✅ **App Filho** para receber e executar comandos
- ✅ **WebSocket** para comunicação em tempo real
