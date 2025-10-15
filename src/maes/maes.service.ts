import { Injectable, ConflictException, NotFoundException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { PrismaService } from '../prisma/prisma.service';
import { CreateMaeDto, MaeResponseDto } from '../common/dto/mae.dto';

@Injectable()
export class MaesService {
  constructor(private prisma: PrismaService) { }

  async create(createMaeDto: CreateMaeDto): Promise<MaeResponseDto> {
    const { nome, email, senha } = createMaeDto;

    // Verificar se email já existe
    const existingMae = await this.prisma.mae.findUnique({
      where: { email },
    });

    if (existingMae) {
      throw new ConflictException('Email já está em uso');
    }

    // Hash da senha
    const hashedSenha = await bcrypt.hash(senha, 10);

    const mae = await this.prisma.mae.create({
      data: {
        nome,
        email,
        senha: hashedSenha,
      },
    });

    // Remover senha da resposta
    const { senha: _, ...maeResponse } = mae;
    return maeResponse;
  }

  async findByEmail(email: string) {
    return this.prisma.mae.findUnique({
      where: { email },
    });
  }

  async findById(id: string) {
    return this.prisma.mae.findUnique({
      where: { id },
      include: {
        filhos: {
          select: {
            id: true,
            nome: true,
            email: true,
            validade: true,
            createdAt: true,
          },
        },
      },
    });
  }

  async getNome(id: string): Promise<{ nome: string }> {
    const mae = await this.prisma.mae.findUnique({
      where: { id },
      select: { nome: true },
    });

    if (!mae) {
      throw new NotFoundException('Mãe não encontrada');
    }

    return { nome: mae.nome };
  }
}






