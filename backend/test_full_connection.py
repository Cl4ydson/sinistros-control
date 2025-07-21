#!/usr/bin/env python3

import pyodbc
import sys
import traceback
from datetime import datetime

def test_connection(name, conn_str):
    """Test database connection"""
    print(f"\n=== TESTANDO {name} ===")
    print(f"Connection String: {conn_str}")
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        conn.close()
        
        print(f"OK {name}: SUCESSO - {result[0]}")
        return True
    except Exception as e:
        print(f"ERRO {name}: ERRO - {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_query_sinistros():
    """Test sinistros query"""
    print(f"\n=== TESTANDO QUERY DE SINISTROS ===")
    
    conn_str = "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        sql = """
        SELECT DISTINCT TOP 2
            RTRIM(OCN.nr_NotaFiscal) AS nota_fiscal,
            CASE WHEN UPPER(RTRIM(MOV.nr_Conhecimento)) = ''
                 THEN RTRIM(MOV.nr_Minuta)
                 ELSE UPPER(RTRIM(MOV.nr_Conhecimento))
            END AS nr_conhecimento,
            RTRIM(MOV.ds_Remetente) AS remetente,
            RTRIM(MOV.ds_Cliente) AS cliente,
            MOV.dt_Coleta AS data_coleta,
            RTRIM(OCO.ds_Ocorrencia) AS tipo_ocorrencia
        FROM tbdOcorrenciaNota OCN WITH (NOLOCK)
        INNER JOIN tbdOcorrencia OCO WITH (NOLOCK) ON OCN.id_Ocorrencia = OCO.id_Ocorrencia
        INNER JOIN tbdMovimento MOV WITH (NOLOCK) ON OCN.id_Movimento = MOV.id_Movimento
        WHERE OCO.ds_Ocorrencia IN (
            'AVARIA PARCIAL','AVARIA TOTAL',
            'EXTRAVIO TOTAL','EXTRAVIO PARCIAL', 
            'ROUBO DE CARGA','MERCADORIA SINISTRADA'
        )
        ORDER BY MOV.dt_Coleta DESC
        """
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        print(f"OK QUERY SINISTROS: SUCESSO - {len(rows)} sinistros encontrados")
        
        for i, row in enumerate(rows):
            print(f"  Sinistro {i+1}: NF={row[0]}, Conh={row[1]}, Cliente={row[3]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERRO QUERY SINISTROS: ERRO - {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_esinistros_table():
    """Test eSinistros table"""
    print(f"\n=== TESTANDO TABELA eSinistros ===")
    
    conn_str = "DRIVER={SQL Server};SERVER=SRVTOTVS02;DATABASE=AUTOMACAO_BRSAMOR;UID=adm;PWD=(Br$amor#2020);TrustServerCertificate=yes;"
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'eSinistros'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if table_exists:
            print("OK Tabela eSinistros existe")
            
            # Count records
            cursor.execute("SELECT COUNT(*) FROM [dbo].[eSinistros]")
            count = cursor.fetchone()[0]
            print(f"OK Total de registros: {count}")
            
        else:
            print("AVISO Tabela eSinistros NAO existe - sera criada automaticamente")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERRO TABELA eSinistros: ERRO - {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    print("=== TESTE COMPLETO DE CONEXÕES ===")
    print(f"Data/Hora: {datetime.now()}")
    
    # Test both databases
    consulta_conn = "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
    automacao_conn = "DRIVER={SQL Server};SERVER=SRVTOTVS02;DATABASE=AUTOMACAO_BRSAMOR;UID=adm;PWD=(Br$amor#2020);TrustServerCertificate=yes;"
    
    results = []
    results.append(test_connection("BANCO CONSULTA", consulta_conn))
    results.append(test_connection("BANCO AUTOMACAO", automacao_conn))
    results.append(test_query_sinistros())
    results.append(test_esinistros_table())
    
    print(f"\n=== RESUMO ===")
    print(f"Testes realizados: {len(results)}")
    print(f"Sucessos: {sum(results)}")
    print(f"Falhas: {len(results) - sum(results)}")
    
    if all(results):
        print("OK TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("ERRO ALGUNS TESTES FALHARAM!")
        return 1

if __name__ == "__main__":
    sys.exit(main())