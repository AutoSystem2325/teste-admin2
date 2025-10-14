import { IsEmail, IsString, MinLength } from 'class-validator';

export class LoginMaeDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  senha: string;
}

export class LoginFilhoDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  senha: string;
}

export class AuthResponseDto {
  access_token: string;
  user: {
    id: string;
    nome: string;
    email: string;
    tipo: 'mae' | 'filho';
    validade?: Date;
  };
}





