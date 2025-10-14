import { Controller, Post, Body, Get, Param, Patch, UseGuards } from '@nestjs/common';
import { FilhosService } from './filhos.service';
import { CreateFilhoDto, UpdateValidadeDto } from '../common/dto/filho.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@Controller('filhos')
export class FilhosController {
  constructor(private readonly filhosService: FilhosService) {}

  @Post()
  @UseGuards(JwtAuthGuard)
  async create(@Body() createFilhoDto: CreateFilhoDto) {
    return this.filhosService.create(createFilhoDto);
  }

  @Get(':maeId')
  @UseGuards(JwtAuthGuard)
  async findByMaeId(@Param('maeId') maeId: string) {
    return this.filhosService.findByMaeId(maeId);
  }

  @Patch(':id/validade')
  @UseGuards(JwtAuthGuard)
  async updateValidade(
    @Param('id') id: string,
    @Body() updateValidadeDto: UpdateValidadeDto,
  ) {
    return this.filhosService.updateValidade(id, updateValidadeDto);
  }
}





