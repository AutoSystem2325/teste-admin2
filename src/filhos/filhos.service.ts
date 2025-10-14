import { Injectable, ConflictException, NotFoundException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { PrismaService } from '../prisma/prisma.service';
import { CreateFilhoDto, UpdateValidadeDto, FilhoResponseDto } from '../common/dto/filho.dto';

@Injectable()
export class FilhosService {
  constructor(private prisma: PrismaService) {}

  async create(createFilhoDto: CreateFilhoDto): Promise<FilhoResponseDto> {
    const { nome, email, senha, maeId, validade } = createFilhoDto;

    // Verificar se a mãe existe
    const mae = await this.prisma.mae.findUnique({
      where: { id: maeId },
    });

    if (!mae) {
      throw new NotFoundException('Mãe não encontrada');
    }

    // Verificar se email já existe
    const existingFilho = await this.prisma.filho.findUnique({
      where: { email },
    });

    if (existingFilho) {
      throw new ConflictException('Email já está em uso');
    }

    // Hash da senha
    const hashedSenha = await bcrypt.hash(senha, 10);

    const filho = await this.prisma.filho.create({
      data: {
        nome,
        email,
        senha: hashedSenha,
        maeId,
        validade: new Date(validade),
      },
      include: {
        mae: {
          select: {
            id: true,
            nome: true,
            email: true,
          },
        },
      },
    });

    // Remover senha da resposta
    const { senha: _, ...filhoResponse } = filho;
    return filhoResponse;
  }

  async findByMaeId(maeId: string): Promise<FilhoResponseDto[]> {
    const filhos = await this.prisma.filho.findMany({
      where: { maeId },
      include: {
        mae: {
          select: {
            id: true,
            nome: true,
            email: true,
          },
        },
      },
    });

    // Remover senhas das respostas
    return filhos.map(({ senha, ...filho }) => filho);
  }

  async updateValidade(id: string, updateValidadeDto: UpdateValidadeDto): Promise<FilhoResponseDto> {
    const { validade } = updateValidadeDto;

    const filho = await this.prisma.filho.findUnique({
      where: { id },
    });

    if (!filho) {
      throw new NotFoundException('Filho não encontrado');
    }

    const updatedFilho = await this.prisma.filho.update({
      where: { id },
      data: {
        validade: new Date(validade),
      },
      include: {
        mae: {
          select: {
            id: true,
            nome: true,
            email: true,
          },
        },
      },
    });

    // Remover senha da resposta
    const { senha: _, ...filhoResponse } = updatedFilho;
    return filhoResponse;
  }

  async findByEmail(email: string) {
    return this.prisma.filho.findUnique({
      where: { email },
      include: { mae: true },
    });
  }

  async findById(id: string) {
    return this.prisma.filho.findUnique({
      where: { id },
      include: { mae: true },
    });
  }

  async findActiveByMaeId(maeId: string) {
    const agora = new Date();
    return this.prisma.filho.findMany({
      where: {
        maeId,
        validade: {
          gt: agora,
        },
      },
    });
  }
}





