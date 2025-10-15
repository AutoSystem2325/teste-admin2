import { IsEmail, IsString, MinLength, IsDateString, IsOptional } from 'class-validator';

export class CreateFilhoDto {
  @IsString()
  @MinLength(2)
  nome: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  senha: string;

  @IsString()
  maeId: string;

  @IsDateString()
  validade: string;
}

export class UpdateValidadeDto {
  @IsDateString()
  validade: string;
}

export class FilhoResponseDto {
  id: string;
  nome: string;
  email: string;
  validade: Date;
  maeId: string;
  createdAt: Date;
  updatedAt: Date;
  mae?: {
    id: string;
    nome: string;
    email: string;
  };
}






