#!/usr/bin/env python3
"""
Script de teste para verificar a conexão com o banco e o repositório
"""

import sys
import traceback
from app.repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC

def test_connection():
    """Testa a conexão com o banco"""
    try:
        print("🔄 Testando conexão com o banco...")
        repo = SinistroRepositoryPyODBC()
        
        # Teste de conexão
        if repo.test_connection():
            print("✅ Conexão com banco OK!")
        else:
            print("❌ Falha na conexão com banco")
            return False
        
        # Teste de busca de sinistros (limitado)
        print("\n🔄 Testando busca de sinistros...")
        sinistros = repo.buscar_sinistros(limit=5)
        print(f"✅ Encontrados {len(sinistros)} sinistros (teste)")
        
        if sinistros:
            print("\n📋 Exemplo de sinistro:")
            primeiro = sinistros[0]
            for key, value in primeiro.items():
                print(f"  {key}: {value}")
        
        # Teste sem limite (primeiros 100 para não sobrecarregar)
        print("\n🔄 Testando busca SEM limite (primeiros 100)...")
        sinistros_all = repo.buscar_sinistros(limit=100)
        print(f"✅ Encontrados {len(sinistros_all)} sinistros (com limit 100)")
        
        # Estatísticas
        print("\n🔄 Testando estatísticas...")
        stats = repo.obter_estatisticas()
        print(f"✅ Estatísticas: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        print("📋 Traceback completo:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do repositório de sinistros")
    print("=" * 50)
    
    success = test_connection()
    
    print("=" * 50)
    if success:
        print("✅ Todos os testes passaram!")
        sys.exit(0)
    else:
        print("❌ Alguns testes falharam!")
        sys.exit(1) 