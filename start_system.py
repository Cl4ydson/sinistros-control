#!/usr/bin/env python3
"""
Script para iniciar o sistema completo (backend + frontend)
"""

import subprocess
import sys
import os
import time
import threading
import signal

def run_backend():
    """Executa o backend"""
    print("🚀 Iniciando backend...")
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "run.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no backend: {e}")
    finally:
        os.chdir("..")

def run_frontend():
    """Executa o frontend"""
    print("🚀 Iniciando frontend...")
    try:
        os.chdir("frontend")
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no frontend: {e}")
    finally:
        os.chdir("..")

def main():
    """Função principal"""
    print("🎯 Sistema de Controle de Sinistros BRSAMOR")
    print("="*50)
    print("Iniciando sistema completo...\n")
    
    # Verificar se as dependências estão instaladas
    print("🔧 Verificando dependências...")
    
    # Verificar backend
    if not os.path.exists("backend/requirements.txt"):
        print("❌ Backend não encontrado!")
        return 1
    
    # Verificar frontend
    if not os.path.exists("frontend/package.json"):
        print("❌ Frontend não encontrado!")
        return 1
    
    print("✅ Dependências OK\n")
    
    # Criar threads para backend e frontend
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    
    try:
        # Iniciar backend
        backend_thread.start()
        print("⏳ Aguardando backend inicializar...")
        time.sleep(3)
        
        # Iniciar frontend
        frontend_thread.start()
        print("⏳ Aguardando frontend inicializar...")
        time.sleep(2)
        
        print("\n🎉 Sistema iniciado com sucesso!")
        print("📱 Frontend: http://localhost:5173")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 Documentação: http://localhost:8000/docs")
        print("\n⚠️  Pressione Ctrl+C para parar o sistema")
        
        # Manter o script rodando
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Parando sistema...")
        print("✅ Sistema parado com sucesso!")
        return 0

if __name__ == "__main__":
    exit(main())