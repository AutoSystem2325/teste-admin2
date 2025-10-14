export interface JwtPayload {
  sub: string;
  email: string;
  tipo: 'mae' | 'filho';
  validade?: Date;
}





