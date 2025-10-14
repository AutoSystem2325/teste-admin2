import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module';
import { AuthModule } from './auth/auth.module';
import { MaesModule } from './maes/maes.module';
import { FilhosModule } from './filhos/filhos.module';
import { RealtimeModule } from './realtime/realtime.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    PrismaModule,
    AuthModule,
    MaesModule,
    FilhosModule,
    RealtimeModule,
  ],
})
export class AppModule {}
