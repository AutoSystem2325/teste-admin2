# =========================
# Etapa 1: Build
# =========================
FROM node:18-alpine AS builder

# Dependências do sistema
RUN apk add --no-cache openssl

WORKDIR /app

# Copiar apenas package.json primeiro (cache)
COPY package*.json ./

# Instalar dependências (incluindo dev)
RUN npm ci

# Copiar resto do projeto
COPY . .

# Gerar Prisma Client
RUN npx prisma generate

# Build do NestJS
RUN npm run build

# Verificação (debug opcional)
RUN ls -la dist && test -f dist/main.js


# =========================
# Etapa 2: Produção
# =========================
FROM node:18-alpine

RUN apk add --no-cache openssl

WORKDIR /app

# Copiar apenas o necessário
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/prisma ./prisma
COPY --from=builder /app/node_modules ./node_modules

# (Opcional) Reinstalar só deps de produção
# RUN npm ci --omit=dev

# Gerar Prisma Client em runtime
RUN npx prisma generate

# Porta (Railway usa env, mas ok expor)
EXPOSE 3000

# Start correto
CMD ["node", "dist/main.js"]
