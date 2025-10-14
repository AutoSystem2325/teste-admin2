import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';
import { HttpExceptionFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Configuração de CORS para permitir conexões WebSocket
  app.enableCors({
    origin: true,
    credentials: true,
  });

  // Filtro global de exceções
  app.useGlobalFilters(new HttpExceptionFilter());

  // Pipe global para validação
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }));

  const port = process.env.PORT || 3000;
  await app.listen(port);
  
  console.log(`🚀 OctavioSync API rodando na porta ${port}`);
  console.log(`📡 WebSocket disponível em ws://localhost:${port}`);
  console.log(`📚 Documentação disponível em http://localhost:${port}`);
  console.log(`🔍 Health check disponível em http://localhost:${port}/health`);
}

bootstrap();
