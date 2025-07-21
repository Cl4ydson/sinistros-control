#!/usr/bin/env python3

import pyodbc
import sys

def test_different_connection_strings():
    """Testa diferentes formatos de string de conexão"""
    
    # Diferentes variações das credenciais
    test_configs = [
        {
            "name": "Formato Original",
            "conn_str": "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
        },
        {
            "name": "Com aspas na senha",
            "conn_str": "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD='Br$Samor@2025#C';TrustServerCertificate=yes;"
        },
        {
            "name": "Sem TrustServerCertificate",
            "conn_str": "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=Br$Samor@2025#C;"
        },
        {
            "name": "Com Trusted_Connection",
            "conn_str": "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;Trusted_Connection=no;UID=consulta.pbi;PWD=Br$Samor@2025#C;"
        },
        {
            "name": "Testando usuario pbi",
            "conn_str": "DRIVER={SQL Server};SERVER=137.131.246.149;DATABASE=dtbTransporte;UID=pbi;PWD=Br$Samor@2025#C;TrustServerCertificate=yes;"
        }
    ]
    
    for config in test_configs:
        print(f"\n=== {config['name']} ===")
        print(f"Connection string: {config['conn_str']}")
        
        try:
            conn = pyodbc.connect(config['conn_str'])
            cursor = conn.cursor()
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            conn.close()
            print(f"SUCCESS: {result[0]}")
            return True  # Primeira conexão que funcionar, para por aqui
            
        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            
            # Analisar o tipo de erro
            if "Login failed" in error_msg:
                print("  -> Problema de autenticação (usuário/senha)")
            elif "Nome da fonte de dados" in error_msg:
                print("  -> Problema com driver ODBC")
            elif "timeout" in error_msg.lower():
                print("  -> Problema de conectividade de rede")
            elif "does not exist" in error_msg:
                print("  -> Banco de dados não existe")
    
    print(f"\nNenhuma configuração funcionou!")
    return False

if __name__ == "__main__":
    test_different_connection_strings()