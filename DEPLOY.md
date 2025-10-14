# 🚀 Deploy no Railway

## Pré-requisitos
- ✅ Banco Neon configurado
- ✅ Código no GitHub
- ✅ Conta no Railway

## Passos para Deploy

### 1. Conectar Repositório
1. Acesse [railway.app](https://railway.app)
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Escolha este repositório

### 2. Configurar Variáveis de Ambiente
No Railway, vá em **Variables** e adicione:

```env
DATABASE_URL=postgresql://neondb_owner:npg_T7KB2YEcZkOr@ep-wild-lab-acgb0uf0-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
JWT_SECRET=octavio-sync-super-secret-jwt-key-2025
JWT_EXPIRES_IN=7d
PORT=3000
NODE_ENV=production
```

### 3. Deploy Automático
- Railway detectará automaticamente que é um projeto Node.js
- Usará o arquivo `railway.json` para configurações
- Build será executado automaticamente
- Deploy será feito com `npm run start:prod`

### 4. Verificar Deploy
Após o deploy, você receberá uma URL como:
```
https://seu-projeto.railway.app
```

### 5. Testar API
```bash
# Teste básico
curl https://seu-projeto.railway.app

# Deve retornar:
{
  "message": "OctavioSync API",
  "version": "1.0.0",
  "status": "running"
}
```

## 🔧 Configurações do Railway

### Build Command
```bash
npm run build
```

### Start Command  
```bash
npm run start:prod
```

### Health Check
```
GET /health
```

## 📝 Próximos Passos

Após deploy bem-sucedido:

1. **Atualizar config.py** nos mini-apps:
   ```python
   SERVER_URL = "https://seu-projeto.railway.app"
   WEBSOCKET_URL = "wss://seu-projeto.railway.app"
   ```

2. **Testar conexão** dos apps Python

3. **Criar primeira mãe** via app ou API

4. **Gerar executáveis** com PyInstaller

## 🐛 Troubleshooting

### Erro de Build
- Verificar se todas as dependências estão no `package.json`
- Verificar se `prisma generate` está sendo executado

### Erro de Conexão DB
- Verificar se `DATABASE_URL` está correta
- Verificar se Neon permite conexões externas

### Erro de WebSocket
- Railway suporta WebSocket automaticamente
- Verificar se porta está correta (Railway usa PORT dinâmico)

## 📊 Monitoramento

Railway fornece:
- ✅ Logs em tempo real
- ✅ Métricas de CPU/RAM
- ✅ Health checks automáticos
- ✅ SSL automático
- ✅ Deploy automático via Git