#!/usr/bin/env python3
"""
Teste da API de sinistros
"""

import requests
import json
import time

def test_api():
    """Testa a API de sinistros"""
    base_url = "http://127.0.0.1:8001"
    
    print("🔄 Testando API de Sinistros...")
    
    # Teste 1: Health check
    try:
        print("\n1. Testando health check...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check falhou: {e}")
        return False
    
    # Teste 2: Root endpoint
    try:
        print("\n2. Testando endpoint raiz...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint falhou: {e}")
        return False
    
    # Teste 3: Test connection
    try:
        print("\n3. Testando conexão com banco...")
        response = requests.get(f"{base_url}/sinistros/test/connection", timeout=10)
        print(f"✅ Test connection: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Dados: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Test connection falhou: {e}")
        return False
    
    # Teste 4: Listar sinistros (limitado)
    try:
        print("\n4. Testando listar sinistros (limit=5)...")
        response = requests.get(f"{base_url}/sinistros?limit=5", timeout=30)
        print(f"✅ Listar sinistros: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                total = data['data']['total']
                sinistros = len(data['data']['sinistros'])
                print(f"📊 Total de sinistros: {total}")
                print(f"📋 Sinistros retornados: {sinistros}")
                if sinistros > 0:
                    primeiro = data['data']['sinistros'][0]
                    print(f"🔍 Primeiro sinistro: {primeiro['nota_fiscal']} - {primeiro['cliente']}")
            else:
                print(f"❌ API retornou erro: {data}")
    except Exception as e:
        print(f"❌ Listar sinistros falhou: {e}")
        return False
    
    # Teste 5: Estatísticas
    try:
        print("\n5. Testando estatísticas...")
        response = requests.get(f"{base_url}/sinistros/estatisticas/resumo", timeout=10)
        print(f"✅ Estatísticas: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Estatísticas: {json.dumps(data['data'], indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Estatísticas falharam: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Teste da API de Sinistros")
    print("=" * 50)
    
    # Aguardar um pouco para API iniciar
    print("⏳ Aguardando API iniciar...")
    time.sleep(3)
    
    success = test_api()
    
    print("=" * 50)
    if success:
        print("✅ API está funcionando corretamente!")
    else:
        print("❌ API tem problemas!") 