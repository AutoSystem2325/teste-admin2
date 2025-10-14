# Dockerfile para OctavioSync API
FROM node:18-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./

# Instalar todas as dependências (incluindo dev dependencies para build)
RUN npm ci

# Copiar código fonte
COPY . .

# Gerar cliente Prisma
RUN npx prisma generate

# Compilar aplicação
RUN npm run build

# Debug: verificar se os arquivos foram gerados
RUN ls -la dist/

# Remover dev dependencies após build
RUN npm prune --production

# Expor porta
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["npm", "run", "start:prod"]





