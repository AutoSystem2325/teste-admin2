#!/usr/bin/env python3
"""
Teste do WebSocket para verificar se o status da mãe está sendo enviado
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

from websocket_client import OctavioSyncWebSocketClient
import time

def test_mae_status():
    print("🧪 TESTE DE STATUS DA MÃE")
    print("=" * 40)
    
    # Simular cliente filho
    ws_client = OctavioSyncWebSocketClient("http://localhost:3000", "fake_token")
    
    def on_mae_status(data):
        print(f"📊 Status da mãe recebido: {data}")
    
    def on_comando(data):
        print(f"📨 Comando recebido: {data}")
    
    # Configurar callbacks
    ws_client.on_mae_status_broadcast(on_mae_status)
    ws_client.on_filho_sync(on_comando)
    
    try:
        print("🔌 Conectando...")
        if ws_client.connect():
            print("✅ Conectado!")
            print("⏳ Aguardando mensagens por 30 segundos...")
            print("   (Execute a mãe e inicie/pare a detecção)")
            
            time.sleep(30)
            
        else:
            print("❌ Falha na conexão")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        ws_client.disconnect()
        print("🔌 Desconectado")

if __name__ == "__main__":
    test_mae_status()