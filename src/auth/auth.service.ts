import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';
import { PrismaService } from '../prisma/prisma.service';
import { LoginMaeDto, LoginFilhoDto, AuthResponseDto } from '../common/dto/auth.dto';
import { JwtPayload } from '../common/interfaces/jwt-payload.interface';
import { ValidadeExpiredException } from '../common/exceptions/validade-expired.exception';

@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
  ) {}

  async loginMae(loginMaeDto: LoginMaeDto): Promise<AuthResponseDto> {
    const { email, senha } = loginMaeDto;

    const mae = await this.prisma.mae.findUnique({
      where: { email },
    });

    if (!mae || !(await bcrypt.compare(senha, mae.senha))) {
      throw new UnauthorizedException('Credenciais inválidas');
    }

    const payload: JwtPayload = {
      sub: mae.id,
      email: mae.email,
      tipo: 'mae',
    };

    const access_token = this.jwtService.sign(payload);

    return {
      access_token,
      user: {
        id: mae.id,
        nome: mae.nome,
        email: mae.email,
        tipo: 'mae',
      },
    };
  }

  async loginFilho(loginFilhoDto: LoginFilhoDto): Promise<AuthResponseDto> {
    const { email, senha } = loginFilhoDto;

    const filho = await this.prisma.filho.findUnique({
      where: { email },
      include: { mae: true },
    });

    if (!filho || !(await bcrypt.compare(senha, filho.senha))) {
      throw new UnauthorizedException('Credenciais inválidas');
    }

    // Verificar validade
    const agora = new Date();
    if (agora > filho.validade) {
      throw new ValidadeExpiredException(filho.validade, agora);
    }

    const payload: JwtPayload = {
      sub: filho.id,
      email: filho.email,
      tipo: 'filho',
      validade: filho.validade,
    };

    const access_token = this.jwtService.sign(payload);

    return {
      access_token,
      user: {
        id: filho.id,
        nome: filho.nome,
        email: filho.email,
        tipo: 'filho',
        validade: filho.validade,
      },
    };
  }

  async validateUser(payload: JwtPayload) {
    if (payload.tipo === 'mae') {
      const mae = await this.prisma.mae.findUnique({
        where: { id: payload.sub },
      });
      return mae ? { ...mae, tipo: 'mae' } : null;
    } else {
      const filho = await this.prisma.filho.findUnique({
        where: { id: payload.sub },
        include: { mae: true },
      });
      
      if (!filho) return null;
      
      // Verificar validade novamente
      const agora = new Date();
      if (agora > filho.validade) {
        return null;
      }
      
      return { ...filho, tipo: 'filho' };
    }
  }
}


