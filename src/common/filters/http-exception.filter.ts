import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { Request, Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    const status = exception.getStatus();

    const exceptionResponse = exception.getResponse();
    
    // Se a exceção já tem uma resposta estruturada (como ValidadeExpiredException), usar ela
    if (typeof exceptionResponse === 'object' && exceptionResponse !== null) {
      const responseObj = exceptionResponse as any;
      
      // Se já tem status, mensagem e detalhes, usar a resposta original
      if (responseObj.status && responseObj.mensagem) {
        console.error(`❌ ${request.method} ${request.url} - ${status} - ${responseObj.mensagem}`);
        return response.status(status).json(responseObj);
      }
    }

    // Para outras exceções, usar o formato padrão
    const message = typeof exceptionResponse === 'string' 
      ? exceptionResponse 
      : (exceptionResponse as any).message || 'Erro interno do servidor';

    const errorResponse = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      method: request.method,
      message: Array.isArray(message) ? message : [message],
    };

    console.error(`❌ ${request.method} ${request.url} - ${status} - ${message}`);

    response.status(status).json(errorResponse);
  }
}


