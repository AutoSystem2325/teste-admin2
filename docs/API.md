# OctavioSync API - Documentação

## Visão Geral

A OctavioSync API é um backend construído com NestJS que gerencia o sistema de sincronização entre Mães e Filhos, com comunicação em tempo real via WebSocket.

## Autenticação

Todos os endpoints protegidos requerem um token JWT no header:
```
Authorization: Bearer <token>
```

## Endpoints REST

### Autenticação

#### POST /auth/login-mae
Login de uma Mãe no sistema.

**Request Body:**
```json
{
  "email": "mae@exemplo.com",
  "senha": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "clh123456789",
    "nome": "Maria Silva",
    "email": "mae@exemplo.com",
    "tipo": "mae"
  }
}
```

#### POST /auth/login-filho
Login de um Filho no sistema.

**Request Body:**
```json
{
  "email": "filho@exemplo.com",
  "senha": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "clh987654321",
    "nome": "João Silva",
    "email": "filho@exemplo.com",
    "tipo": "filho",
    "validade": "2024-02-15T00:00:00.000Z"
  }
}
```

**Erro de Validade Expirada:**
```json
{
  "status": "expired",
  "mensagem": "Licença expirada",
  "detalhes": {
    "dataExpiracao": "2024-12-31T23:59:59.000Z",
    "dataAtual": "2025-01-10T00:20:47.527Z",
    "diasExpirado": 10,
    "mensagemDetalhada": "Sua licença expirou há 10 dia(s). Entre em contato com a administração para renovar."
  }
}
```

### Mães

#### POST /maes
Cadastrar uma nova Mãe.

**Request Body:**
```json
{
  "nome": "Maria Silva",
  "email": "mae@exemplo.com",
  "senha": "123456"
}
```

**Response:**
```json
{
  "id": "clh123456789",
  "nome": "Maria Silva",
  "email": "mae@exemplo.com",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z"
}
```

#### GET /maes/:id
Buscar uma Mãe por ID (requer autenticação).

**Response:**
```json
{
  "id": "clh123456789",
  "nome": "Maria Silva",
  "email": "mae@exemplo.com",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z",
  "filhos": [
    {
      "id": "clh987654321",
      "nome": "João Silva",
      "email": "joao@exemplo.com",
      "validade": "2024-02-15T00:00:00.000Z",
      "createdAt": "2024-01-15T10:30:00.000Z"
    }
  ]
}
```

### Filhos

#### POST /filhos
Cadastrar um novo Filho (requer autenticação).

**Request Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@exemplo.com",
  "senha": "123456",
  "maeId": "clh123456789",
  "validade": "2024-02-15T00:00:00.000Z"
}
```

**Response:**
```json
{
  "id": "clh987654321",
  "nome": "João Silva",
  "email": "joao@exemplo.com",
  "validade": "2024-02-15T00:00:00.000Z",
  "maeId": "clh123456789",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z",
  "mae": {
    "id": "clh123456789",
    "nome": "Maria Silva",
    "email": "mae@exemplo.com"
  }
}
```

#### GET /filhos/:maeId
Listar todos os filhos de uma Mãe (requer autenticação).

**Response:**
```json
[
  {
    "id": "clh987654321",
    "nome": "João Silva",
    "email": "joao@exemplo.com",
    "validade": "2024-02-15T00:00:00.000Z",
    "maeId": "clh123456789",
    "createdAt": "2024-01-15T10:30:00.000Z",
    "updatedAt": "2024-01-15T10:30:00.000Z",
    "mae": {
      "id": "clh123456789",
      "nome": "Maria Silva",
      "email": "mae@exemplo.com"
    }
  }
]
```

#### PATCH /filhos/:id/validade
Atualizar a validade de um Filho (requer autenticação).

**Request Body:**
```json
{
  "validade": "2024-03-15T00:00:00.000Z"
}
```

**Response:**
```json
{
  "id": "clh987654321",
  "nome": "João Silva",
  "email": "joao@exemplo.com",
  "validade": "2024-03-15T00:00:00.000Z",
  "maeId": "clh123456789",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z",
  "mae": {
    "id": "clh123456789",
    "nome": "Maria Silva",
    "email": "mae@exemplo.com"
  }
}
```

## WebSocket Events

### Conexão

Para conectar ao WebSocket, envie o token JWT na autenticação:

```javascript
const socket = io('ws://localhost:3000', {
  auth: {
    token: 'your-jwt-token'
  }
});
```

### Eventos do Cliente

#### auth
Reautenticação via token JWT.

**Payload:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### mae:update
Mãe envia padrão detectado (apenas para Mães).

**Payload:**
```json
{
  "padrao": "1C"
}
```

**Padrões suportados:**
- `"1C"` - Padrão 1C
- `"1V"` - Padrão 1V
- `"-"` - Padrão neutro

#### filho:status
Filho envia status ON/OFF (apenas para Filhos).

**Payload:**
```json
{
  "status": "ON"
}
```

### Eventos do Servidor

#### auth
Confirmação de autenticação.

**Payload:**
```json
{
  "status": "success",
  "user": {
    "id": "clh123456789",
    "email": "mae@exemplo.com",
    "tipo": "mae",
    "maeId": "clh123456789",
    "validade": null
  }
}
```

**Erro de autenticação:**
```json
{
  "status": "error",
  "mensagem": "Token inválido"
}
```

**Erro de validade expirada:**
```json
{
  "status": "expired",
  "mensagem": "Licença expirada"
}
```

#### filho:sync
Sincronização de dados para Filhos (quando Mãe envia mae:update).

**Payload:**
```json
{
  "padrao": "1C",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "maeId": "clh123456789"
}
```

#### filho:status:confirmed
Confirmação de status enviado pelo Filho.

**Payload:**
```json
{
  "status": "ON",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### error
Mensagens de erro.

**Payload:**
```json
{
  "message": "Apenas mães podem enviar atualizações"
}
```

## Códigos de Status HTTP

- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Dados inválidos
- `401` - Não autorizado
- `404` - Não encontrado
- `409` - Conflito (email já existe)
- `500` - Erro interno do servidor

## Exemplos de Uso

### Fluxo Completo

1. **Cadastrar Mãe:**
```bash
curl -X POST http://localhost:3000/maes \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria Silva","email":"mae@exemplo.com","senha":"123456"}'
```

2. **Login da Mãe:**
```bash
curl -X POST http://localhost:3000/auth/login-mae \
  -H "Content-Type: application/json" \
  -d '{"email":"mae@exemplo.com","senha":"123456"}'
```

3. **Cadastrar Filho:**
```bash
curl -X POST http://localhost:3000/filhos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"nome":"João Silva","email":"joao@exemplo.com","senha":"123456","maeId":"<mae-id>","validade":"2024-02-15T00:00:00.000Z"}'
```

4. **Login do Filho:**
```bash
curl -X POST http://localhost:3000/auth/login-filho \
  -H "Content-Type: application/json" \
  -d '{"email":"joao@exemplo.com","senha":"123456"}'
```

5. **Conectar WebSocket e enviar dados:**
```javascript
// Mãe conecta e envia padrão
const maeSocket = io('ws://localhost:3000', {
  auth: { token: maeToken }
});

maeSocket.emit('mae:update', { padrao: '1C' });

// Filho conecta e recebe sincronização
const filhoSocket = io('ws://localhost:3000', {
  auth: { token: filhoToken }
});

filhoSocket.on('filho:sync', (data) => {
  console.log('Padrão recebido:', data.padrao);
});
```


