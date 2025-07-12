#!/usr/bin/env python3
"""
Script de teste para verificar conectividade com tabela eSinistros
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_esinistros_connection():
    """
    Testa conectividade com a tabela eSinistros
    """
    try:
        # String de conexão para AUTOMACAO_BRSAMOR
        # Ajustar conforme sua configuração
        DATABASE_URL = "mssql+pyodbc://servidor/AUTOMACAO_BRSAMOR?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        
        # Criar engine
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Testar conexão
        with SessionLocal() as session:
            logger.info("🔍 Testando conectividade com banco AUTOMACAO_BRSAMOR...")
            
            # 1. Verificar se tabela eSinistros existe
            logger.info("📋 Verificando existência da tabela eSinistros...")
            
            query = text("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'eSinistros'")
            result = session.execute(query)
            table_exists = result.scalar()
            
            if table_exists > 0:
                logger.info("✅ Tabela eSinistros encontrada!")
                
                # 2. Contar registros
                logger.info("📊 Contando registros na tabela...")
                count_query = text("SELECT COUNT(*) FROM eSinistros")
                count_result = session.execute(count_query)
                total_records = count_result.scalar()
                
                logger.info(f"📈 Total de registros: {total_records}")
                
                # 3. Testar consulta de amostra
                logger.info("🔎 Testando consulta de amostra...")
                sample_query = text("""
                    SELECT TOP 5 
                        [Nota Fiscal],
                        [Minu.Conh],
                        [CLIENTE],
                        [STATUS SINISTRO],
                        [VALOR DO SINISTRO ]
                    FROM eSinistros
                    ORDER BY [Data Cadastro] DESC
                """)
                
                sample_result = session.execute(sample_query)
                rows = sample_result.fetchall()
                
                logger.info("📋 Amostra de dados:")
                for i, row in enumerate(rows, 1):
                    logger.info(f"  {i}. Nota: {getattr(row, 'Nota Fiscal', 'N/A')} | "
                              f"Cliente: {getattr(row, 'CLIENTE', 'N/A')} | "
                              f"Status: {getattr(row, 'STATUS SINISTRO', 'N/A')}")
                
                # 4. Testar permissões de escrita (cuidadoso)
                logger.info("🔐 Testando permissões de escrita...")
                
                try:
                    # Tentar uma operação de escrita segura (sem modificar dados reais)
                    test_query = text("SELECT 1 WHERE 1=0")  # Query que não retorna nada
                    session.execute(test_query)
                    logger.info("✅ Permissões de consulta OK")
                    
                    # Para testar escrita real, descomente as linhas abaixo com CUIDADO:
                    # insert_test = text("INSERT INTO eSinistros ([Nota Fiscal]) VALUES ('TEST_DELETE_ME')")
                    # session.execute(insert_test)
                    # delete_test = text("DELETE FROM eSinistros WHERE [Nota Fiscal] = 'TEST_DELETE_ME'")
                    # session.execute(delete_test)
                    # session.commit()
                    # logger.info("✅ Permissões de escrita OK")
                    
                except Exception as e:
                    logger.warning(f"⚠️ Possível limitação de escrita: {e}")
                
                logger.info("🎉 Teste concluído com sucesso!")
                return True
                
            else:
                logger.error("❌ Tabela eSinistros não encontrada!")
                
                # Listar tabelas disponíveis
                logger.info("📋 Listando tabelas disponíveis:")
                tables_query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
                tables_result = session.execute(tables_query)
                tables = tables_result.fetchall()
                
                for table in tables:
                    logger.info(f"  - {table[0]}")
                
                return False
    
    except Exception as e:
        logger.error(f"❌ Erro na conectividade: {e}")
        return False

def test_fallback_connection():
    """
    Testa conectividade com banco de consulta (fallback)
    """
    try:
        logger.info("🔄 Testando fallback para banco de consulta...")
        
        # Importar e testar repositório de consulta
        from backend.app.repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
        
        repo = SinistroRepositoryPyODBC()
        sinistros = repo.listar_sinistros()
        
        if sinistros:
            logger.info(f"✅ Fallback OK - {len(sinistros)} sinistros encontrados")
            return True
        else:
            logger.warning("⚠️ Fallback retornou lista vazia")
            return False
    
    except Exception as e:
        logger.error(f"❌ Erro no fallback: {e}")
        return False

def main():
    """
    Executa todos os testes
    """
    logger.info("🚀 Iniciando testes de conectividade...")
    logger.info("=" * 60)
    
    # Teste 1: Tabela eSinistros
    esinistros_ok = test_esinistros_connection()
    
    logger.info("=" * 60)
    
    # Teste 2: Fallback
    fallback_ok = test_fallback_connection()
    
    logger.info("=" * 60)
    
    # Resumo
    logger.info("📊 RESUMO DOS TESTES:")
    logger.info(f"  🏢 Tabela eSinistros: {'✅ OK' if esinistros_ok else '❌ FALHA'}")
    logger.info(f"  🔄 Fallback consulta: {'✅ OK' if fallback_ok else '❌ FALHA'}")
    
    if esinistros_ok or fallback_ok:
        logger.info("🎉 Sistema funcional!")
        return True
    else:
        logger.error("💥 Sistema com problemas!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 