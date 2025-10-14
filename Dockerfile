# Etapa de build
FROM node:18-alpine AS builder

# Instalar dependências do sistema
RUN apk add --no-cache openssl

WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./
COPY prisma ./prisma/

# Instalar todas as dependências (incluindo dev)
RUN npm ci

# Gerar cliente Prisma
RUN npx prisma generate

# Copiar código fonte
COPY . .

# Compilar aplicação
RUN npm run build

# Verificar se o build foi bem-sucedido
RUN ls -la dist/src/ && test -f dist/src/main.js

# Etapa de produção
FROM node:18-alpine

# Instalar dependências do sistema
RUN apk add --no-cache openssl

WORKDIR /app

# Copiar arquivos compilados da etapa anterior
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/prisma ./prisma
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma

# Instalar apenas dependências de produção
RUN npm ci --omit=dev

# Gerar cliente Prisma novamente (necessário para produção)
RUN npx prisma generate

# Expor porta
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["node", "dist/src/main.js"]





