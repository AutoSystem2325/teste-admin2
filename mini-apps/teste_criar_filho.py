#!/usr/bin/env python3
"""
Teste simples para criar filho
"""

import sys
import os

# Adicionar o diretório shared ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

from api_client import OctavioSyncAPIClient
from config import SERVER_URL

def teste_criar_filho():
    """Teste de criação de filho"""
    
    # Dados de exemplo baseados no JSON que você mostrou
    mae_data = {
        "nome": "João Mãe",
        "email": "joaomae@exemplo.com", 
        "senha": "123456"
    }
    
    filho_data = {
        "nome": "João Silva Novo",
        "email": "joao.novo@exemplo.com",
        "senha": "123456",
        "validade": "2025-12-31"
    }
    
    print("🧪 Testando criação de filho...")
    
    # Criar cliente API
    client = OctavioSyncAPIClient(SERVER_URL)
    
    # 1. Login da mãe
    print(f"1. Fazendo login da mãe: {mae_data['email']}")
    if not client.login_mae(mae_data['email'], mae_data['senha']):
        print("❌ Falha no login da mãe")
        return
    
    print("✅ Login da mãe bem-sucedido!")
    
    # 2. Pegar ID da mãe
    mae_id = client.get_user_id()
    print(f"📋 ID da mãe: {mae_id}")
    
    # 3. Criar filho
    print(f"2. Criando filho: {filho_data['nome']}")
    if client.criar_filho(
        filho_data['nome'],
        filho_data['email'], 
        filho_data['senha'],
        mae_id,
        filho_data['validade']
    ):
        print("✅ Filho criado com sucesso!")
        print(f"📧 Email: {filho_data['email']}")
        print(f"📅 Validade: {filho_data['validade']}")
    else:
        print("❌ Falha ao criar filho")

if __name__ == "__main__":
    teste_criar_filho()