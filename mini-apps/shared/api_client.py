"""
Cliente API REST compartilhado para os mini apps
"""
import requests
import json
import logging
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OctavioSyncAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.user_info = None
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     headers: Optional[Dict] = None) -> Optional[Dict]:
        """Faz requisição HTTP"""
        url = f"{self.base_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        headers['Content-Type'] = 'application/json'
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == 'PATCH':
                response = self.session.patch(url, json=data, headers=headers)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro na requisição {method} {endpoint}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"❌ Detalhes do erro: {error_data}")
                except:
                    logger.error(f"❌ Resposta de erro: {e.response.text}")
            return None
    
    def login_mae(self, email: str, senha: str) -> bool:
        """Login de Mãe"""
        data = {
            'email': email,
            'senha': senha
        }
        
        response = self._make_request('POST', '/auth/login-mae', data)
        
        if response and 'access_token' in response:
            self.token = response['access_token']
            self.user_info = response['user']
            logger.info(f"✅ Login Mãe bem-sucedido: {self.user_info['email']}")
            return True
        
        logger.error("❌ Falha no login da Mãe")
        return False
    
    def login_filho(self, email: str, senha: str) -> bool:
        """Login de Filho"""
        data = {
            'email': email,
            'senha': senha
        }
        
        response = self._make_request('POST', '/auth/login-filho', data)
        
        if response and 'access_token' in response:
            self.token = response['access_token']
            self.user_info = response['user']
            logger.info(f"✅ Login Filho bem-sucedido: {self.user_info['email']}")
            return True
        
        logger.error("❌ Falha no login do Filho")
        return False
    
    def cadastrar_mae(self, nome: str, email: str, senha: str) -> bool:
        """Cadastrar nova Mãe"""
        data = {
            'nome': nome,
            'email': email,
            'senha': senha
        }
        
        response = self._make_request('POST', '/maes', data)
        
        if response and 'id' in response:
            logger.info(f"✅ Mãe cadastrada: {response['email']}")
            return True
        
        logger.error("❌ Falha no cadastro da Mãe")
        return False
    
    def cadastrar_filho(self, nome: str, email: str, senha: str, mae_id: str) -> bool:
        """Cadastrar novo Filho"""
        data = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'maeId': mae_id
        }
        
        response = self._make_request('POST', '/filhos', data)
        
        if response and 'id' in response:
            logger.info(f"✅ Filho cadastrado: {response['email']}")
            return True
        
        logger.error("❌ Falha no cadastro do Filho")
        return False
    
    def listar_filhos(self, mae_id: str) -> Optional[list]:
        """Listar filhos de uma Mãe"""
        response = self._make_request('GET', f'/filhos/{mae_id}')
        
        if response:
            logger.info(f"✅ Listados {len(response)} filhos")
            return response
        
        logger.error("❌ Falha ao listar filhos")
        return None
    
    def atualizar_validade_filho(self, filho_id: str, validade: str) -> bool:
        """Atualizar validade de um Filho"""
        data = {
            'validade': validade
        }
        
        response = self._make_request('PATCH', f'/filhos/{filho_id}/validade', data)
        
        if response and 'id' in response:
            logger.info(f"✅ Validade atualizada para: {response['validade']}")
            return True
        
        logger.error("❌ Falha ao atualizar validade")
        return False
    
    def get_token(self) -> Optional[str]:
        """Retorna o token atual"""
        return self.token
    
    def get_user_info(self) -> Optional[Dict]:
        """Retorna informações do usuário atual"""
        return self.user_info
    
    def get_filho_id(self) -> Optional[str]:
        """Retorna o ID do filho logado"""
        if self.user_info and 'id' in self.user_info:
            return str(self.user_info['id'])
        return None
    
    def get_user_id(self) -> Optional[str]:
        """Retorna o ID do usuário logado (mãe ou filho)"""
        if self.user_info and 'id' in self.user_info:
            return str(self.user_info['id'])
        return None
    
    def criar_filho(self, nome: str, email: str, senha: str, mae_id: str, validade: str) -> bool:
        """Criar novo filho com validade"""
        data = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'maeId': mae_id,
            'validade': validade
        }
        
        response = self._make_request('POST', '/filhos', data)
        
        if response and 'id' in response:
            logger.info(f"✅ Filho criado: {response['email']}")
            return True
        
        logger.error("❌ Falha ao criar filho")
        return False
    
    def is_authenticated(self) -> bool:
        """Verifica se está autenticado"""
        return self.token is not None



