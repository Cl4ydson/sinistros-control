"""
Teste direto da conexão e query do banco de dados
"""

import pyodbc
import sys
import traceback

def test_connection():
    """Testa conexão direta com o banco"""
    
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
    
    print("🔧 Testando conexão direta com o banco...")
    print(f"Connection String: {conn_str}")
    
    try:
        # Teste de conexão
        print("\n1. Testando conexão...")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Teste básico
        print("2. Executando SELECT 1...")
        cursor.execute("SELECT 1 as teste")
        result = cursor.fetchone()
        print(f"   Resultado: {result[0]}")
        
        # Teste das tabelas
        print("\n3. Verificando se as tabelas existem...")
        tables_to_check = [
            'tbdOcorrenciaNota',
            'tbdOcorrencia', 
            'tbdMovimento'
        ]
        
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT TOP 1 * FROM {table}")
                cursor.fetchone()
                print(f"   ✅ Tabela {table}: OK")
            except Exception as e:
                print(f"   ❌ Tabela {table}: ERRO - {e}")
        
        # Teste da query de sinistros
        print("\n4. Testando query de sinistros...")
        
        sql = """
        SELECT DISTINCT TOP 5
            RTRIM(OCN.nr_NotaFiscal) AS nota_fiscal,
            CASE WHEN UPPER(RTRIM(MOV.nr_Conhecimento)) = ''
                 THEN RTRIM(MOV.nr_Minuta)
                 ELSE UPPER(RTRIM(MOV.nr_Conhecimento))
            END AS nr_conhecimento,
            RTRIM(MOV.ds_Remetente) AS remetente,
            RTRIM(MOV.ds_Cliente) AS cliente,
            MOV.dt_Coleta AS data_coleta,
            RTRIM(OCO.ds_Ocorrencia) AS tipo_ocorrencia,
            RTRIM(OCN.ds_Ocorrencia) AS descricao_ocorrencia
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
        
        print("   Executando query...")
        cursor.execute(sql)
        
        # Obter colunas
        columns = [column[0] for column in cursor.description]
        print(f"   Colunas: {columns}")
        
        # Obter resultados
        results = cursor.fetchall()
        print(f"   Registros encontrados: {len(results)}")
        
        if results:
            print("\n   Primeiros registros:")
            for i, row in enumerate(results[:3]):
                print(f"   Registro {i+1}:")
                for j, value in enumerate(row):
                    print(f"     {columns[j]}: {value}")
                print()
        else:
            print("   ⚠️ Nenhum registro encontrado!")
            
            # Vamos verificar se há dados nas tabelas
            print("\n5. Verificando dados nas tabelas...")
            
            # Contar registros em cada tabela
            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   {table}: {count} registros")
                except Exception as e:
                    print(f"   {table}: ERRO - {e}")
            
            # Verificar tipos de ocorrência disponíveis
            print("\n6. Verificando tipos de ocorrência...")
            try:
                cursor.execute("SELECT DISTINCT ds_Ocorrencia FROM tbdOcorrencia ORDER BY ds_Ocorrencia")
                ocorrencias = cursor.fetchall()
                print(f"   Total de tipos: {len(ocorrencias)}")
                print("   Tipos encontrados:")
                for oc in ocorrencias[:10]:  # Mostrar apenas os primeiros 10
                    print(f"     - {oc[0]}")
                if len(ocorrencias) > 10:
                    print(f"     ... e mais {len(ocorrencias) - 10} tipos")
            except Exception as e:
                print(f"   ERRO ao verificar ocorrências: {e}")
        
        conn.close()
        print("\n✅ Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO no teste: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        print("Traceback completo:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_connection()