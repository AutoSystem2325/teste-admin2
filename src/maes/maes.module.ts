import { Module } from '@nestjs/common';
import { MaesService } from './maes.service';
import { MaesController } from './maes.controller';

@Module({
  providers: [MaesService],
  controllers: [MaesController],
  exports: [MaesService],
})
export class MaesModule {}





