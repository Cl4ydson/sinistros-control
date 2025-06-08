#!/usr/bin/env python3
"""
Script completo para iniciar o sistema de sinistros
"""

import sys
import os
import subprocess
import time
import signal
import threading
from pathlib import Path

def run_backend():
    """Inicia o backend"""
    print("🚀 Iniciando Backend...")
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    # Iniciar a API
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000", 
        "--reload"
    ])

def run_frontend():
    """Inicia o frontend"""
    print("🚀 Iniciando Frontend...")
    frontend_path = Path(__file__).parent / "frontend"
    os.chdir(frontend_path)
    
    # Instalar dependências se necessário
    if not (frontend_path / "node_modules").exists():
        print("📦 Instalando dependências do frontend...")
        subprocess.run(["npm", "install"])
    
    # Iniciar o frontend
    subprocess.run(["npm", "run", "dev"])

def main():
    """Função principal"""
    print("🎯 Sistema de Gestão de Sinistros")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    current_dir = Path.cwd()
    if not (current_dir / "backend").exists() or not (current_dir / "frontend").exists():
        print("❌ Execute este script na pasta raiz do projeto!")
        sys.exit(1)
    
    try:
        # Iniciar backend em thread separada
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Aguardar um pouco para o backend iniciar
        print("⏳ Aguardando backend iniciar...")
        time.sleep(5)
        
        # Iniciar frontend (processo principal)
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n👋 Encerrando sistema...")
        sys.exit(0)

if __name__ == "__main__":
    main() 