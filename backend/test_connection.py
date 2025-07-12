import pyodbc

def list_drivers():
    print("Drivers ODBC disponíveis:")
    for driver in pyodbc.drivers():
        print(f"  - {driver}")

def test_connection():
    connection_strings = [
        # Formato 1: Padrão
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=181.41.182.168,37000;"
        "DATABASE=CUYZ6N_117556_PR_PD;"
        "UID=CLT117557-READ;"
        "PWD=A)FS(dBZ2,,1J:u;>7x&",
        
        # Formato 2: Com caracteres escapados
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=181.41.182.168,37000;"
        "DATABASE=CUYZ6N_117556_PR_PD;"
        "UID=CLT117557-READ;"
        "PWD={A)FS(dBZ2,,1J:u;>7x&}",
        
        # Formato 3: Com aspas
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=181.41.182.168,37000;'
        'DATABASE=CUYZ6N_117556_PR_PD;'
        'UID=CLT117557-READ;'
        'PWD="A)FS(dBZ2,,1J:u;>7x&"',

        # Formato 4: Porta separada
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=181.41.182.168;"
        "PORT=37000;"
        "DATABASE=CUYZ6N_117556_PR_PD;"
        "UID=CLT117557-READ;"
        "PWD=A)FS(dBZ2,,1J:u;>7x&"
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        try:
            print(f"\nTentando formato {i}...")
            conn = pyodbc.connect(conn_str)
            print("✅ Conexão estabelecida com sucesso!")
            
            cursor = conn.cursor()
            cursor.execute("SELECT @@version")
            version = cursor.fetchone()[0]
            print(f"\nVersão do SQL Server:\n{version}")
            
            conn.close()
            return  # Se chegou aqui, deu certo
        except pyodbc.Error as e:
            print(f"❌ Erro: {str(e)}")
    
    print("\n❌ Nenhum formato de conexão funcionou.")

if __name__ == "__main__":
    list_drivers()
    test_connection() 