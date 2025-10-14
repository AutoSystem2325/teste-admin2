# OctavioSync API

Backend central do sistema OctavioSync construído com NestJS, TypeScript, Prisma ORM e PostgreSQL.

## 🏗️ Arquitetura

- **NestJS** com TypeScript
- **Prisma ORM** com PostgreSQL
- **JWT** para autenticação
- **Socket.IO** para comunicação em tempo real
- **bcrypt** para hash de senhas

## 📦 Módulos

- `auth` → Autenticação (JWT)
- `maes` → Cadastro de Mães
- `filhos` → Cadastro de Filhos (com relação com Mães)
- `validade` → Controle de datas de validade
- `realtime` → Comunicação WebSocket (Socket.IO)

## 🚀 Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
npm install
```

3. Configure as variáveis de ambiente:
```bash
cp env.example .env
```

4. Configure o banco de dados PostgreSQL e atualize a `DATABASE_URL` no arquivo `.env`

5. Execute as migrações do Prisma:
```bash
npm run prisma:migrate
```

6. Execute o seed (opcional):
```bash
npm run prisma:seed
```

7. Inicie o servidor:
```bash
npm run start:dev
```

## 📡 Endpoints REST

### Autenticação
- `POST /auth/login-mae` - Login de Mãe
- `POST /auth/login-filho` - Login de Filho

### Mães
- `POST /maes` - Cadastrar Mãe
- `GET /maes/:id` - Buscar Mãe por ID

### Filhos
- `POST /filhos` - Cadastrar Filho
- `GET /filhos/:maeId` - Listar filhos de uma Mãe
- `PATCH /filhos/:id/validade` - Atualizar validade de um Filho

## 🔌 WebSocket Events

### Eventos do Cliente
- `auth` - Autenticação via token JWT
- `mae:update` - Mãe envia padrão detectado (1C, 1V, -)
- `filho:status` - Filho envia status ON/OFF

### Eventos do Servidor
- `auth` - Confirmação de autenticação
- `filho:sync` - Sincronização de dados para filhos
- `filho:status:confirmed` - Confirmação de status
- `error` - Mensagens de erro

## 🔐 Autenticação

Todos os endpoints protegidos requerem o header:
```
Authorization: Bearer <token>
```

Para WebSocket, envie o token na conexão:
```javascript
const socket = io('ws://localhost:3000', {
  auth: {
    token: 'your-jwt-token'
  }
});
```

## 📊 Controle de Validade

Quando um Filho faz login, o servidor verifica a data de validade:
- Se `Date.now() > validade`, retorna erro: `{ "status": "expired", "mensagem": "Licença expirada" }`
- Caso contrário, permite login normal

## 🌐 Fluxo WebSocket

1. **App Mãe** faz login → servidor autentica → conecta ao socket
2. Ao detectar padrão visual (1C, 1V, -), **App Mãe** emite `mae:update`
3. **Servidor** repassa esse padrão em tempo real a todos os **Filhos** conectados àquela Mãe
4. Se algum **Filho** tiver validade expirada, é desconectado e não recebe dados
5. Todos os eventos são logados no console do servidor

## 🧪 Dados de Teste

Após executar o seed, você terá:

**Mãe:**
- Email: `mae@exemplo.com`
- Senha: `123456`

**Filhos:**
- Email: `filho1@exemplo.com` (validade: 30 dias)
- Email: `filho2@exemplo.com` (validade: 15 dias)
- Senha: `123456`

## 📝 Scripts Disponíveis

### Desenvolvimento
- `npm run start:dev` - Inicia em modo desenvolvimento
- `npm run build` - Compila o projeto
- `npm run lint` - Executa o linter
- `npm run format` - Formata o código

### Prisma
- `npm run prisma:generate` - Gera o cliente Prisma
- `npm run prisma:migrate` - Executa migrações
- `npm run prisma:studio` - Abre o Prisma Studio
- `npm run prisma:seed` - Executa o seed

### Docker
- `npm run docker:up` - Inicia serviços de produção
- `npm run docker:down` - Para serviços de produção
- `npm run docker:logs` - Visualiza logs de produção
- `npm run docker:dev` - Inicia serviços de desenvolvimento
- `npm run docker:dev:down` - Para serviços de desenvolvimento
- `npm run docker:dev:logs` - Visualiza logs de desenvolvimento

## 🐳 Docker

### Executar com Docker Compose

#### Produção (com aplicação)
```bash
# Iniciar todos os serviços
npm run docker:up

# Ver logs
npm run docker:logs

# Parar serviços
npm run docker:down
```

#### Desenvolvimento (apenas banco + Adminer)
```bash
# Iniciar banco e Adminer para desenvolvimento
npm run docker:dev

# Ver logs
npm run docker:dev:logs

# Parar serviços
npm run docker:dev:down
```

### Serviços disponíveis:

#### Produção:
- **API:** http://localhost:3000
- **Adminer:** http://localhost:8080
- **PostgreSQL:** localhost:5432

#### Desenvolvimento:
- **Adminer:** http://localhost:8081
- **PostgreSQL:** localhost:5433

### Configuração do Adminer:

1. Acesse http://localhost:8080 (produção) ou http://localhost:8081 (desenvolvimento)
2. **Sistema:** PostgreSQL
3. **Servidor:** postgres
4. **Usuário:** postgres
5. **Senha:** postgres
6. **Base de dados:** octavio_sync (produção) ou octavio_sync_dev (desenvolvimento)

## 🔧 Configuração de Desenvolvimento

O servidor roda na porta 3000 por padrão. Para alterar, modifique a variável `PORT` no arquivo `.env`.

WebSocket disponível em: `ws://localhost:3000`
