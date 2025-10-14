import { Module } from '@nestjs/common';
import { FilhosService } from './filhos.service';
import { FilhosController } from './filhos.controller';

@Module({
  providers: [FilhosService],
  controllers: [FilhosController],
  exports: [FilhosService],
})
export class FilhosModule {}





