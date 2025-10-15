import { Controller, Post, Body, HttpCode, HttpStatus, Get } from '@nestjs/common';
import { AuthService } from './auth.service';
import { LoginMaeDto, LoginFilhoDto } from '../common/dto/auth.dto';
import { CreateMaeDto } from '../common/dto/mae.dto';

@Controller()
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Get()
  getHello(): object {
    return {
      message: 'OctavioSync API',
      version: '1.0.0',
      status: 'running',
      timestamp: new Date().toISOString(),
      endpoints: {
        auth: {
          'POST /auth/login-mae': 'Login de Mãe',
          'POST /auth/login-filho': 'Login de Filho',
        },
        admin: {
          'POST /admin/login-master': 'Login Master Admin',
          'POST /admin/create-mae': 'Criar Mãe (Master Only)',
          'POST /admin/create-filho': 'Criar Filho (Master Only)',
          'GET /admin/maes': 'Listar todas as Mães (Master Only)',
          'GET /admin/filhos': 'Listar todos os Filhos (Master Only)',
        },
        api: {
          'GET /api/names/:userId/:userType': 'Buscar nomes da Mãe e Filho',
        },
        maes: {
          'POST /maes': 'Cadastrar Mãe',
          'GET /maes/:id': 'Buscar Mãe por ID',
        },
        filhos: {
          'POST /filhos': 'Cadastrar Filho',
          'GET /filhos/:maeId': 'Listar filhos de uma Mãe',
          'PATCH /filhos/:id/validade': 'Atualizar validade de um Filho',
        },
        websocket: {
          url: 'ws://localhost:3000',
          events: [
            'auth',
            'mae:update',
            'filho:status',
            'filho:sync',
            'filho:status:confirmed',
            'error',
          ],
        },
      },
    };
  }

  @Get('health')
  getHealth(): object {
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      memory: process.memoryUsage(),
    };
  }

  @Post('auth/login-mae')
  @HttpCode(HttpStatus.OK)
  async loginMae(@Body() loginMaeDto: LoginMaeDto) {
    return this.authService.loginMae(loginMaeDto);
  }

  @Post('auth/login-filho')
  @HttpCode(HttpStatus.OK)
  async loginFilho(@Body() loginFilhoDto: LoginFilhoDto) {
    return this.authService.loginFilho(loginFilhoDto);
  }
}
