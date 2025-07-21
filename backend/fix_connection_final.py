#!/usr/bin/env python3
"""
SOLUÇÃO FINAL - Script para corrigir conexões em produção
Execute este script para testar e corrigir as conexões definitivamente
"""

import pyodbc
import sys
import os

def main():
    print("=== SOLUÇÃO FINAL PARA CONEXÕES ===\n")
    
    # 1. Verificar drivers disponíveis
    print("1. Drivers ODBC disponíveis:")
    drivers = pyodbc.drivers()
    for i, driver in enumerate(drivers, 1):
        print(f"   {i}. {driver}")
    
    if "SQL Server" not in drivers:
        print("❌ ERRO: Driver 'SQL Server' não encontrado!")
        print("   Instale o driver SQL Server Native Client")
        return False
    
    # 2. Testar conexão com banco de consulta
    print("\n2. Testando banco de CONSULTA...")
    conn_str_consulta = "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
    
    try:
        conn = pyodbc.connect(conn_str_consulta)
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 RTRIM(OCN.nr_NotaFiscal) FROM tbdOcorrenciaNota OCN")
        result = cursor.fetchone()
        conn.close()
        print(f"   ✅ SUCCESS: Conectado! Primeira NF: {result[0]}")
    except Exception as e:
        print(f"   ❌ ERRO: {str(e)}")
        return False
    
    # 3. Testar conexão com banco de automação  
    print("\n3. Testando banco de AUTOMAÇÃO...")
    conn_str_automacao = "DRIVER={SQL Server};SERVER=SRVTOTVS02;DATABASE=AUTOMACAO_BRSAMOR;UID=adm;PWD=(Br$amor#2020);TrustServerCertificate=yes;"
    
    try:
        conn = pyodbc.connect(conn_str_automacao)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='eSinistros'")
        result = cursor.fetchone()
        conn.close()
        table_exists = result[0] > 0
        print(f"   ✅ SUCCESS: Conectado! Tabela eSinistros existe: {table_exists}")
    except Exception as e:
        print(f"   ❌ ERRO: {str(e)}")
        return False
    
    # 4. Testar repository
    print("\n4. Testando Repository...")
    try:
        sys.path.append(os.path.dirname(__file__))
        from app.repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
        
        repo = SinistroRepositoryPyODBC()
        sinistros = repo.buscar_sinistros(limit=1)
        print(f"   ✅ SUCCESS: Repository OK! {len(sinistros)} sinistros encontrados")
        
        if sinistros:
            s = sinistros[0]
            print(f"   📄 Primeiro sinistro: NF {s['nota_fiscal']} - {s['cliente']}")
            
    except Exception as e:
        print(f"   ❌ ERRO no Repository: {str(e)}")
        return False
    
    print("\n" + "="*50)
    print("🎉 TODAS AS CONEXÕES ESTÃO FUNCIONANDO!")
    print("="*50)
    print("\nPARA USAR EM PRODUÇÃO:")
    print("1. Pare o servidor atual")
    print("2. Execute: uvicorn app.main:app --host 0.0.0.0 --port 8003")
    print("3. Teste: http://localhost:8003/sinistros/test/connection")
    print("\nSe ainda não funcionar no servidor web,")
    print("o problema é de permissões ou ambiente do processo web.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)