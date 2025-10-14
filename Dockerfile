# Dockerfile para OctavioSync API
FROM node:18-alpine

# Instalar dependências do sistema
RUN apk add --no-cache openssl

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./
COPY prisma ./prisma/

# Instalar todas as dependências
RUN npm ci

# Gerar cliente Prisma
RUN npx prisma generate

# Copiar código fonte
COPY . .

# Compilar aplicação
RUN npm run build

# Debug: verificar estrutura de arquivos
RUN echo "=== Conteúdo da pasta dist ===" && ls -la dist/ || echo "Pasta dist não existe"
RUN echo "=== Conteúdo da pasta raiz ===" && ls -la

# Verificar se o arquivo main.js existe
RUN test -f dist/main.js && echo "main.js encontrado!" || echo "main.js NÃO encontrado!"

# Remover dev dependencies após build
RUN npm prune --production

# Expor porta
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["node", "dist/main.js"]





