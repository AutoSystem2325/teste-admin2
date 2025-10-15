import { IsEmail, IsString, MinLength } from 'class-validator';

export class CreateMaeDto {
  @IsString()
  @MinLength(2)
  nome: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  senha: string;
}

export class MaeResponseDto {
  id: string;
  nome: string;
  email: string;
  createdAt: Date;
  updatedAt: Date;
}






