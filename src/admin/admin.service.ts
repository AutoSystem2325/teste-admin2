import { PrismaService } from '@/prisma/prisma.service';
import { Injectable, UnauthorizedException, ConflictException, NotFoundException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';

export interface LoginAdminDto {
  email: string;
  senha: string;
}

export interface CreateMaeDto {
  nome: string;
  email: string;
  senha: string;
}

export interface CreateFilhoDto {
  nome: string;
  email: string;
  senha: string;
  maeId: string;
  validade: string;
}

export interface CreateAdminDto {
  nome: string;
  email: string;
  senha: string;
  isMaster?: boolean;
}

export interface UpdateMaeDto {
  nome?: string;
  email?: string;
  senha?: string;
}

export interface UpdateFilhoDto {
  nome?: string;
  email?: string;
  senha?: string;
  validade?: string;
}

export interface AuthResponseDto {
  access_token: string;
  user: {
    id: string;
    nome: string;
    email: string;
    tipo: string;
    isMaster?: boolean;
  };
}

export interface NamesResponseDto {
  maeNome: string;
  filhoNome: string;
  maeId: string;
  filhoId: string;
}

@Injectable()
export class AdminService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
  ) { }

  async loginMasterAdmin(loginAdminDto: LoginAdminDto): Promise<AuthResponseDto> {
    const { email, senha } = loginAdminDto;

    // Buscar admin no banco
    const admin = await this.prisma.admin.findUnique({
      where: { email },
    });

    if (!admin || !(await bcrypt.compare(senha, admin.senha))) {
      throw new UnauthorizedException('Credenciais inválidas');
    }

    if (!admin.isMaster) {
      throw new UnauthorizedException('Acesso negado: não é master admin');
    }

    const payload = {
      sub: admin.id,
      email: admin.email,
      tipo: 'master_admin',
      isMaster: admin.isMaster,
    };

    const access_token = this.jwtService.sign(payload);

    return {
      access_token,
      user: {
        id: admin.id,
        nome: admin.nome,
        email: admin.email,
        tipo: 'master_admin',
        isMaster: admin.isMaster,
      },
    };
  }

  async createMae(createMaeDto: CreateMaeDto): Promise<any> {
    const { nome, email, senha } = createMaeDto;

    // Verificar se email já existe
    const existingMae = await this.prisma.mae.findUnique({
      where: { email },
    });

    if (existingMae) {
      throw new ConflictException('Email já está em uso');
    }

    // Hash da senha
    const hashedPassword = await bcrypt.hash(senha, 10);

    // Criar mãe
    const mae = await this.prisma.mae.create({
      data: {
        nome,
        email,
        senha: hashedPassword,
      },
    });

    return {
      id: mae.id,
      nome: mae.nome,
      email: mae.email,
      createdAt: mae.createdAt,
    };
  }

  async createFilho(createFilhoDto: CreateFilhoDto): Promise<any> {
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
    const hashedPassword = await bcrypt.hash(senha, 10);

    // Converter validade para Date
    const validadeDate = new Date(validade);

    // Criar filho
    const filho = await this.prisma.filho.create({
      data: {
        nome,
        email,
        senha: hashedPassword,
        maeId,
        validade: validadeDate,
      },
      include: {
        mae: true,
      },
    });

    return {
      id: filho.id,
      nome: filho.nome,
      email: filho.email,
      validade: filho.validade,
      mae: {
        id: filho.mae.id,
        nome: filho.mae.nome,
        email: filho.mae.email,
      },
      createdAt: filho.createdAt,
    };
  }

  async getAllMaes(): Promise<any[]> {
    const maes = await this.prisma.mae.findMany({
      include: {
        filhos: {
          select: {
            id: true,
            nome: true,
            email: true,
            validade: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    return maes;
  }

  async getAllFilhos(): Promise<any[]> {
    const filhos = await this.prisma.filho.findMany({
      include: {
        mae: {
          select: {
            id: true,
            nome: true,
            email: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    return filhos;
  }

  async createAdmin(createAdminDto: CreateAdminDto): Promise<any> {
    const { nome, email, senha, isMaster = false } = createAdminDto;

    // Verificar se email já existe
    const existingAdmin = await this.prisma.admin.findUnique({
      where: { email },
    });

    if (existingAdmin) {
      throw new ConflictException('Email já está em uso');
    }

    // Hash da senha
    const hashedPassword = await bcrypt.hash(senha, 10);

    // Criar admin
    const admin = await this.prisma.admin.create({
      data: {
        nome,
        email,
        senha: hashedPassword,
        isMaster,
      },
    });

    return {
      id: admin.id,
      nome: admin.nome,
      email: admin.email,
      isMaster: admin.isMaster,
      createdAt: admin.createdAt,
    };
  }

  async getAllAdmins(): Promise<any[]> {
    const admins = await this.prisma.admin.findMany({
      select: {
        id: true,
        nome: true,
        email: true,
        isMaster: true,
        createdAt: true,
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    return admins;
  }

  async updateMae(id: string, updateMaeDto: UpdateMaeDto): Promise<any> {
    const { nome, email, senha } = updateMaeDto;

    // Verificar se a mãe existe
    const existingMae = await this.prisma.mae.findUnique({
      where: { id },
    });

    if (!existingMae) {
      throw new NotFoundException('Mãe não encontrada');
    }

    // Se email foi alterado, verificar se não está em uso
    if (email && email !== existingMae.email) {
      const emailInUse = await this.prisma.mae.findUnique({
        where: { email },
      });

      if (emailInUse) {
        throw new ConflictException('Email já está em uso');
      }
    }

    // Preparar dados para atualização
    const updateData: any = {};
    if (nome) updateData.nome = nome;
    if (email) updateData.email = email;
    if (senha) updateData.senha = await bcrypt.hash(senha, 10);

    // Atualizar mãe
    const updatedMae = await this.prisma.mae.update({
      where: { id },
      data: updateData,
    });

    return {
      id: updatedMae.id,
      nome: updatedMae.nome,
      email: updatedMae.email,
      updatedAt: updatedMae.updatedAt,
    };
  }

  async deleteMae(id: string): Promise<any> {
    // Verificar se a mãe existe
    const existingMae = await this.prisma.mae.findUnique({
      where: { id },
      include: {
        filhos: true,
      },
    });

    if (!existingMae) {
      throw new NotFoundException('Mãe não encontrada');
    }

    // Deletar mãe (filhos serão deletados automaticamente por cascade)
    await this.prisma.mae.delete({
      where: { id },
    });

    return {
      message: 'Mãe deletada com sucesso',
      deletedMae: {
        id: existingMae.id,
        nome: existingMae.nome,
        email: existingMae.email,
      },
      deletedFilhos: existingMae.filhos.length,
    };
  }

  async updateFilho(id: string, updateFilhoDto: UpdateFilhoDto): Promise<any> {
    const { nome, email, senha, validade } = updateFilhoDto;

    // Verificar se o filho existe
    const existingFilho = await this.prisma.filho.findUnique({
      where: { id },
      include: { mae: true },
    });

    if (!existingFilho) {
      throw new NotFoundException('Filho não encontrado');
    }

    // Se email foi alterado, verificar se não está em uso
    if (email && email !== existingFilho.email) {
      const emailInUse = await this.prisma.filho.findUnique({
        where: { email },
      });

      if (emailInUse) {
        throw new ConflictException('Email já está em uso');
      }
    }

    // Preparar dados para atualização
    const updateData: any = {};
    if (nome) updateData.nome = nome;
    if (email) updateData.email = email;
    if (senha) updateData.senha = await bcrypt.hash(senha, 10);
    if (validade) updateData.validade = new Date(validade);

    // Atualizar filho
    const updatedFilho = await this.prisma.filho.update({
      where: { id },
      data: updateData,
      include: { mae: true },
    });

    return {
      id: updatedFilho.id,
      nome: updatedFilho.nome,
      email: updatedFilho.email,
      validade: updatedFilho.validade,
      mae: {
        id: updatedFilho.mae.id,
        nome: updatedFilho.mae.nome,
      },
      updatedAt: updatedFilho.updatedAt,
    };
  }

  async deleteFilho(id: string): Promise<any> {
    // Verificar se o filho existe
    const existingFilho = await this.prisma.filho.findUnique({
      where: { id },
      include: { mae: true },
    });

    if (!existingFilho) {
      throw new NotFoundException('Filho não encontrado');
    }

    // Deletar filho
    await this.prisma.filho.delete({
      where: { id },
    });

    return {
      message: 'Filho deletado com sucesso',
      deletedFilho: {
        id: existingFilho.id,
        nome: existingFilho.nome,
        email: existingFilho.email,
        mae: existingFilho.mae.nome,
      },
    };
  }

  async getNames(userId: string, userType: string): Promise<NamesResponseDto> {
    if (userType === 'mae') {
      // Se é mãe, buscar a mãe e um filho dela (primeiro filho)
      const mae = await this.prisma.mae.findUnique({
        where: { id: userId },
        include: {
          filhos: {
            take: 1,
            orderBy: {
              createdAt: 'asc',
            },
          },
        },
      });

      if (!mae) {
        throw new NotFoundException('Mãe não encontrada');
      }

      const filho = mae.filhos[0];
      if (!filho) {
        throw new NotFoundException('Nenhum filho encontrado para esta mãe');
      }

      return {
        maeNome: mae.nome,
        filhoNome: filho.nome,
        maeId: mae.id,
        filhoId: filho.id,
      };
    } else if (userType === 'filho') {
      // Se é filho, buscar o filho e sua mãe
      const filho = await this.prisma.filho.findUnique({
        where: { id: userId },
        include: {
          mae: true,
        },
      });

      if (!filho) {
        throw new NotFoundException('Filho não encontrado');
      }

      return {
        maeNome: filho.mae.nome,
        filhoNome: filho.nome,
        maeId: filho.mae.id,
        filhoId: filho.id,
      };
    } else {
      throw new UnauthorizedException('Tipo de usuário inválido');
    }
  }


}