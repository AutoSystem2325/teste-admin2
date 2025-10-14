import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Iniciando seed do banco de dados...');

  // Criar uma mãe de exemplo
  const mae = await prisma.mae.upsert({
    where: { email: 'mae@exemplo.com' },
    update: {},
    create: {
      nome: 'Maria Silva',
      email: 'mae@exemplo.com',
      senha: await bcrypt.hash('123456', 10),
    },
  });

  console.log('✅ Mãe criada:', mae.email);

  // Criar filhos de exemplo
  const filho1 = await prisma.filho.upsert({
    where: { email: 'filho1@exemplo.com' },
    update: {},
    create: {
      nome: 'João Silva',
      email: 'filho1@exemplo.com',
      senha: await bcrypt.hash('123456', 10),
      maeId: mae.id,
      validade: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 dias
    },
  });

  const filho2 = await prisma.filho.upsert({
    where: { email: 'filho2@exemplo.com' },
    update: {},
    create: {
      nome: 'Ana Silva',
      email: 'filho2@exemplo.com',
      senha: await bcrypt.hash('123456', 10),
      maeId: mae.id,
      validade: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000), // 15 dias
    },
  });

  console.log('✅ Filhos criados:', filho1.email, filho2.email);
  console.log('🎉 Seed concluído com sucesso!');
}

main()
  .catch((e) => {
    console.error('❌ Erro no seed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });





