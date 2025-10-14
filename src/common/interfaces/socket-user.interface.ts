import { Socket } from 'socket.io';

export interface SocketUser extends Socket {
  user: {
    id: string;
    email: string;
    tipo: 'mae' | 'filho';
    maeId?: string;
    validade?: Date;
  };
}





