"""
Teste simples da API
"""

import requests
import time
import subprocess
import sys
import os

def test_api():
    """Testa se a API está respondendo"""
    
    base_url = "http://127.0.0.1:8001"
    
    print("🔧 Testando API na porta 8001...")
    
    # Teste 1: Endpoint raiz
    try:
        print("\n1. Testando endpoint raiz...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Response: {response.json()}")
        else:
            print(f"   ❌ Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Conexão recusada - API não está rodando")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Endpoint de sinistros direto
    try:
        print("\n2. Testando endpoint de teste direto...")
        response = requests.get(f"{base_url}/sinistros/teste-todos", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Total: {data.get('total', 0)}")
            if data.get('sinistros'):
                print(f"   ✅ Primeiro sinistro: {list(data['sinistros'][0].keys())}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Endpoint principal
    try:
        print("\n3. Testando endpoint principal...")
        response = requests.get(f"{base_url}/sinistros/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Tipo de resposta: {type(data)}")
            if isinstance(data, dict):
                print(f"   ✅ Chaves: {list(data.keys())}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    return True

def start_backend_simple():
    """Inicia o backend de forma simples"""
    print("🚀 Iniciando backend...")
    
    # Mudar para o diretório backend
    backend_dir = os.path.join(os.getcwd(), 'backend')
    
    try:
        # Comando para iniciar o backend
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8001",
            "--reload"
        ]
        
        print(f"Executando: {' '.join(cmd)}")
        print(f"Diretório: {backend_dir}")
        
        # Iniciar processo
        process = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguardar um pouco para o servidor iniciar
        time.sleep(5)
        
        # Verificar se o processo ainda está rodando
        if process.poll() is None:
            print("✅ Backend iniciado com sucesso")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend falhou ao iniciar")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {e}")
        return None

if __name__ == "__main__":
    # Primeiro testar se já está rodando
    if not test_api():
        print("\n🔄 API não está rodando, tentando iniciar...")
        process = start_backend_simple()
        
        if process:
            print("\n⏳ Aguardando backend inicializar...")
            time.sleep(10)
            test_api()
        else:
            print("❌ Não foi possível iniciar o backend")
    else:
        print("✅ API já está funcionando!")