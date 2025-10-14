"""
Cliente WebSocket compartilhado para os mini apps
"""
import socketio
import json
import logging
from typing import Callable, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OctavioSyncWebSocketClient:
    def __init__(self, server_url: str, token: str):
        self.server_url = server_url
        self.token = token
        self.sio = socketio.Client()
        self.connected = False
        self.user_info = None
        
        # Configurar eventos
        self._setup_events()
    
    def _setup_events(self):
        """Configura os eventos do WebSocket"""
        
        @self.sio.event
        def connect():
            logger.info("🔌 Conectado ao servidor WebSocket")
            self.connected = True
        
        @self.sio.event
        def disconnect():
            logger.info("🔌 Desconectado do servidor WebSocket")
            self.connected = False
        
        @self.sio.event
        def auth(data):
            if data.get('status') == 'success':
                self.user_info = data.get('user')
                logger.info(f"✅ Autenticação bem-sucedida: {self.user_info.get('email')}")
            else:
                logger.error(f"❌ Erro na autenticação: {data.get('mensagem')}")
        
        @self.sio.event
        def error(data):
            logger.error(f"❌ Erro WebSocket: {data.get('message')}")
    
    def connect(self) -> bool:
        """Conecta ao servidor WebSocket"""
        try:
            self.sio.connect(
                self.server_url,
                auth={'token': self.token}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do servidor WebSocket"""
        if self.connected:
            self.sio.disconnect()
    
    def send_mae_update(self, pattern: str):
        """Envia atualização de padrão (apenas para Mães)"""
        if not self.connected:
            logger.error("❌ Não conectado ao servidor")
            return False
        
        try:
            self.sio.emit('mae:update', {'padrao': pattern})
            logger.info(f"📡 Padrão enviado: {pattern}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao enviar padrão: {e}")
            return False
    
    def send_filho_status(self, status: str):
        """Envia status (apenas para Filhos)"""
        if not self.connected:
            logger.error("❌ Não conectado ao servidor")
            return False
        
        try:
            self.sio.emit('filho:status', {'status': status})
            logger.info(f"📊 Status enviado: {status}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao enviar status: {e}")
            return False
    
    def on_filho_sync(self, callback: Callable):
        """Registra callback para receber sincronização (apenas para Filhos)"""
        def handle_filho_sync(data):
            logger.info(f"📡 Recebeu sincronização: {data.get('padrao')}")
            callback(data)
        
        # Registrar o evento com o nome exato
        self.sio.on('filho:sync', handle_filho_sync)
    
    def on_filho_status_confirmed(self, callback: Callable):
        """Registra callback para confirmação de status (apenas para Filhos)"""
        def handle_status_confirmed(data):
            logger.info(f"✅ Status confirmado: {data.get('status')}")
            callback(data)
        
        # Registrar o evento com o nome exato
        self.sio.on('filho:status:confirmed', handle_status_confirmed)
    
    def on_mae_status_broadcast(self, callback: Callable):
        """Registra callback para receber status da mãe (apenas para Filhos)"""
        def handle_mae_status(data):
            logger.info(f"📊 Status da mãe recebido: {data.get('mae_status')}")
            callback(data)
        
        # Registrar o evento
        self.sio.on('mae_status_broadcast', handle_mae_status)
    
    def is_connected(self) -> bool:
        """Verifica se está conectado"""
        return self.connected
    
    def get_user_info(self) -> Optional[dict]:
        """Retorna informações do usuário"""
        return self.user_info



