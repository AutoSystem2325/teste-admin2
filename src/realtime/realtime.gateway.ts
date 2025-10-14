import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  OnGatewayConnection,
  OnGatewayDisconnect,
  ConnectedSocket,
  MessageBody,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { UseGuards } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../prisma/prisma.service';
import { SocketUser } from '../common/interfaces/socket-user.interface';
import { JwtPayload } from '../common/interfaces/jwt-payload.interface';

@WebSocketGateway({
  cors: {
    origin: '*',
    credentials: true,
  },
})
export class RealtimeGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;

  private connectedUsers = new Map<string, SocketUser>();

  constructor(
    private jwtService: JwtService,
    private configService: ConfigService,
    private prisma: PrismaService,
  ) {}

  async handleConnection(client: SocketUser) {
    try {
      const token = client.handshake.auth?.token || client.handshake.headers?.authorization?.replace('Bearer ', '');
      
      if (!token) {
        console.log('❌ Conexão rejeitada: Token não fornecido');
        client.disconnect();
        return;
      }

      const payload = this.jwtService.verify(token, {
        secret: this.configService.get<string>('JWT_SECRET'),
      }) as JwtPayload;

      // Verificar se o usuário ainda é válido
      let user;
      if (payload.tipo === 'mae') {
        user = await this.prisma.mae.findUnique({
          where: { id: payload.sub },
        });
      } else {
        user = await this.prisma.filho.findUnique({
          where: { id: payload.sub },
          include: { mae: true },
        });

        // Verificar validade para filhos
        if (user && new Date() > user.validade) {
          console.log(`❌ Filho ${user.email} com licença expirada desconectado`);
          client.disconnect();
          return;
        }
      }

      if (!user) {
        console.log('❌ Conexão rejeitada: Usuário não encontrado');
        client.disconnect();
        return;
      }

      // Adicionar informações do usuário ao socket
      client.user = {
        id: user.id,
        email: user.email,
        tipo: payload.tipo,
        maeId: payload.tipo === 'filho' ? user.maeId : user.id,
        validade: payload.tipo === 'filho' ? user.validade : undefined,
      };

      this.connectedUsers.set(client.id, client);

      console.log(`✅ ${payload.tipo === 'mae' ? 'Mãe' : 'Filho'} ${user.email} conectado (${client.id})`);

      // Enviar confirmação de autenticação
      client.emit('auth', {
        status: 'success',
        user: client.user,
      });

    } catch (error) {
      console.log('❌ Erro na autenticação WebSocket:', error.message);
      client.disconnect();
    }
  }

  handleDisconnect(client: SocketUser) {
    if (client.user) {
      console.log(`🔌 ${client.user.tipo === 'mae' ? 'Mãe' : 'Filho'} ${client.user.email} desconectado`);
    }
    this.connectedUsers.delete(client.id);
  }

  @SubscribeMessage('mae:update')
  async handleMaeUpdate(
    @ConnectedSocket() client: SocketUser,
    @MessageBody() data: { padrao: string },
  ) {
    if (!client.user || client.user.tipo !== 'mae') {
      client.emit('error', { message: 'Apenas mães podem enviar atualizações' });
      return;
    }

    console.log(`📡 Mãe ${client.user.email} enviou padrão: ${data.padrao}`);

    // Buscar todos os filhos ativos da mãe
    const filhosAtivos = await this.prisma.filho.findMany({
      where: {
        maeId: client.user.id,
        validade: {
          gt: new Date(),
        },
      },
    });

    // Enviar para todos os filhos conectados da mesma mãe
    const filhosConectados = Array.from(this.connectedUsers.values()).filter(
      (socket) => socket.user?.tipo === 'filho' && socket.user?.maeId === client.user.id,
    );

    console.log(`📤 Enviando padrão para ${filhosConectados.length} filhos conectados`);

    filhosConectados.forEach((filhoSocket) => {
      filhoSocket.emit('filho:sync', {
        padrao: data.padrao,
        timestamp: new Date().toISOString(),
        maeId: client.user.id,
      });
    });

    // Log da ação
    console.log(`✅ Padrão "${data.padrao}" sincronizado com ${filhosConectados.length} filhos`);
  }

  @SubscribeMessage('filho:status')
  async handleFilhoStatus(
    @ConnectedSocket() client: SocketUser,
    @MessageBody() data: { status: 'ON' | 'OFF' },
  ) {
    if (!client.user || client.user.tipo !== 'filho') {
      client.emit('error', { message: 'Apenas filhos podem enviar status' });
      return;
    }

    console.log(`📊 Filho ${client.user.email} status: ${data.status}`);

    // Verificar se ainda está válido
    if (client.user.validade && new Date() > client.user.validade) {
      console.log(`❌ Filho ${client.user.email} com licença expirada desconectado`);
      client.emit('error', { 
        status: 'expired', 
        mensagem: 'Licença expirada' 
      });
      client.disconnect();
      return;
    }

    // Confirmar recebimento do status
    client.emit('filho:status:confirmed', {
      status: data.status,
      timestamp: new Date().toISOString(),
    });
  }

  @SubscribeMessage('auth')
  async handleAuth(
    @ConnectedSocket() client: SocketUser,
    @MessageBody() data: { token: string },
  ) {
    try {
      const payload = this.jwtService.verify(data.token, {
        secret: this.configService.get<string>('JWT_SECRET'),
      }) as JwtPayload;

      // Revalidar usuário
      let user;
      if (payload.tipo === 'mae') {
        user = await this.prisma.mae.findUnique({
          where: { id: payload.sub },
        });
      } else {
        user = await this.prisma.filho.findUnique({
          where: { id: payload.sub },
          include: { mae: true },
        });

        if (user && new Date() > user.validade) {
          client.emit('auth', {
            status: 'expired',
            mensagem: 'Licença expirada',
          });
          return;
        }
      }

      if (!user) {
        client.emit('auth', {
          status: 'error',
          mensagem: 'Usuário não encontrado',
        });
        return;
      }

      // Atualizar informações do usuário
      client.user = {
        id: user.id,
        email: user.email,
        tipo: payload.tipo,
        maeId: payload.tipo === 'filho' ? user.maeId : user.id,
        validade: payload.tipo === 'filho' ? user.validade : undefined,
      };

      client.emit('auth', {
        status: 'success',
        user: client.user,
      });

      console.log(`🔐 Reautenticação bem-sucedida para ${user.email}`);

    } catch (error) {
      client.emit('auth', {
        status: 'error',
        mensagem: 'Token inválido',
      });
    }
  }

  // Método para obter estatísticas de conexões
  getConnectionStats() {
    const stats = {
      total: this.connectedUsers.size,
      maes: 0,
      filhos: 0,
    };

    this.connectedUsers.forEach((socket) => {
      if (socket.user?.tipo === 'mae') {
        stats.maes++;
      } else if (socket.user?.tipo === 'filho') {
        stats.filhos++;
      }
    });

    return stats;
  }
}





