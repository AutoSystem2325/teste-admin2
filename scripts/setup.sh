#!/bin/bash

echo "🚀 Configurando OctavioSync API..."

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale o Node.js primeiro."
    exit 1
fi

# Verificar se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Por favor, instale o npm primeiro."
    exit 1
fi

echo "📦 Instalando dependências..."
npm install

echo "🔧 Configurando variáveis de ambiente..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "✅ Arquivo .env criado. Por favor, configure as variáveis de ambiente."
else
    echo "✅ Arquivo .env já existe."
fi

echo "📊 Gerando cliente Prisma..."
npx prisma generate

echo "🗄️ Executando migrações do banco de dados..."
npx prisma migrate dev --name init

echo "🌱 Executando seed do banco de dados..."
npm run prisma:seed

echo "🎉 Configuração concluída!"
echo ""
echo "Para iniciar o servidor:"
echo "  npm run start:dev"
echo ""
echo "Para acessar o Prisma Studio:"
echo "  npm run prisma:studio"





