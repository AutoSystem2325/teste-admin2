import { Controller, Post, Body, Get, Param, UseGuards } from '@nestjs/common';
import { MaesService } from './maes.service';
import { CreateMaeDto } from '../common/dto/mae.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@Controller('maes')
export class MaesController {
  constructor(private readonly maesService: MaesService) {}

  @Post()
  async create(@Body() createMaeDto: CreateMaeDto) {
    return this.maesService.create(createMaeDto);
  }

  @Get(':id')
  @UseGuards(JwtAuthGuard)
  async findOne(@Param('id') id: string) {
    return this.maesService.findById(id);
  }
}





