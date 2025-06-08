#!/usr/bin/env python3
"""
🎯 SISTEMA DE GESTÃO DE SINISTROS - SOLUÇÃO DEFINITIVA
Conecta aos 8.363+ sinistros do banco SQL Server
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório backend ao Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Agora importar e executar
def main():
    print("🎯 SISTEMA DE GESTÃO DE SINISTROS")
    print("=" * 50)
    print("✅ Banco: dtbTransporte (172.30.0.211)")
    print("✅ Total: ~8.363 sinistros")
    print("✅ API: http://127.0.0.1:8000")
    print("✅ Frontend: Modo API ativo")
    print("=" * 50)
    
    try:
        # Mudar para diretório backend
        os.chdir(backend_path)
        
        # Importar a aplicação
        from app.main import app
        import uvicorn
        
        print("🚀 Iniciando API na porta 8000...")
        print("📖 Documentação: http://127.0.0.1:8000/docs")
        print("🔑 Auth: http://127.0.0.1:8000/auth/register/")
        print("📊 Sinistros: http://127.0.0.1:8000/sinistros")
        print()
        print("🎮 Para usar:")
        print("1. Abra http://127.0.0.1:8000/docs no navegador")
        print("2. Ou use o frontend React")
        print("3. Crie um usuário em /auth/register/")
        print("4. Faça login em /auth/login")
        print("5. Acesse os sinistros em /sinistros")
        print()
        print("⚠️  CTRL+C para parar")
        print("=" * 50)
        
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8000, 
            reload=False,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\n🔧 Diagnóstico:")
        print("1. Verifique se o SQL Server está acessível")
        print("2. Confirme as credenciais do banco")
        print("3. Execute: pip install fastapi uvicorn pyodbc")
        
        # Teste rápido
        print("\n🧪 Teste de conexão:")
        try:
            from app.repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
            repo = SinistroRepositoryPyODBC()
            if repo.test_connection():
                print("✅ Banco OK")
                stats = repo.obter_estatisticas()
                print(f"📊 Total sinistros: {stats['total_sinistros']}")
            else:
                print("❌ Banco FALHOU")
        except Exception as te:
            print(f"❌ Teste falhou: {te}")

if __name__ == "__main__":
    main() 