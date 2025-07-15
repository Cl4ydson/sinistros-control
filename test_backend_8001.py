"""
Teste rápido do backend na porta 8001
"""

import uvicorn
import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

def start_backend():
    """Inicia o backend na porta 8001"""
    print("🚀 Iniciando backend na porta 8001...")
    
    try:
        # Importar a aplicação
        from app.main import app
        print("✅ Aplicação importada com sucesso")
        
        # Iniciar servidor
        uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_backend()