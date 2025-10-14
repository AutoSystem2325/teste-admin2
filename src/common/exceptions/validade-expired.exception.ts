import { UnauthorizedException } from '@nestjs/common';

export class ValidadeExpiredException extends UnauthorizedException {
  constructor(dataExpiracao: Date, dataAtual: Date) {
    const diasExpirado = Math.ceil((dataAtual.getTime() - dataExpiracao.getTime()) / (1000 * 60 * 60 * 24));
    
    super({
      status: 'expired',
      mensagem: 'Licença expirada',
      detalhes: {
        dataExpiracao: dataExpiracao.toISOString(),
        dataAtual: dataAtual.toISOString(),
        diasExpirado: diasExpirado,
        mensagemDetalhada: `Sua licença expirou há ${diasExpirado} dia(s). Entre em contato com a administração para renovar.`
      }
    });
  }
}


