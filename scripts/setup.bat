@echo off
echo 🚀 Configurando OctavioSync API...

REM Verificar se o Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado. Por favor, instale o Node.js primeiro.
    pause
    exit /b 1
)

REM Verificar se o npm está instalado
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm não encontrado. Por favor, instale o npm primeiro.
    pause
    exit /b 1
)

echo 📦 Instalando dependências...
npm install

echo 🔧 Configurando variáveis de ambiente...
if not exist .env (
    copy env.example .env
    echo ✅ Arquivo .env criado. Por favor, configure as variáveis de ambiente.
) else (
    echo ✅ Arquivo .env já existe.
)

echo 📊 Gerando cliente Prisma...
npx prisma generate

echo 🗄️ Executando migrações do banco de dados...
npx prisma migrate dev --name init

echo 🌱 Executando seed do banco de dados...
npm run prisma:seed

echo 🎉 Configuração concluída!
echo.
echo Para iniciar o servidor:
echo   npm run start:dev
echo.
echo Para acessar o Prisma Studio:
echo   npm run prisma:studio
pause





