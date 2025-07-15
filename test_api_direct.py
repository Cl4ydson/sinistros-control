"""
Teste direto da API para verificar se está funcionando
"""

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """Testa os endpoints da API"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🔧 Testando endpoints da API...")
    
    # Teste 1: Endpoint raiz
    print("\n1. Testando endpoint raiz...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Documentação
    print("\n2. Testando documentação...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Documentação disponível")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Endpoint de teste direto
    print("\n3. Testando endpoint de teste direto...")
    try:
        response = requests.get(f"{base_url}/sinistros/teste-todos", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Total de sinistros: {data.get('total', 0)}")
            
            if 'sinistros' in data and data['sinistros']:
                print("   Primeiro sinistro:")
                primeiro = data['sinistros'][0]
                for key, value in primeiro.items():
                    print(f"     {key}: {value}")
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 4: Endpoint principal de sinistros
    print("\n4. Testando endpoint principal de sinistros...")
    try:
        response = requests.get(f"{base_url}/sinistros/", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Resposta recebida")
            print(f"   Tipo: {type(data)}")
            
            if isinstance(data, dict):
                print(f"   Chaves: {list(data.keys())}")
                if 'sinistros' in data:
                    print(f"   Total de sinistros: {len(data['sinistros'])}")
            elif isinstance(data, list):
                print(f"   Total de registros: {len(data)}")
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 5: Endpoint com parâmetros
    print("\n5. Testando endpoint com parâmetros...")
    try:
        params = {"limit": 5}
        response = requests.get(f"{base_url}/sinistros/", params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Resposta com parâmetros recebida")
            if isinstance(data, dict) and 'sinistros' in data:
                print(f"   Sinistros retornados: {len(data['sinistros'])}")
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    return True

if __name__ == "__main__":
    test_api_endpoints()