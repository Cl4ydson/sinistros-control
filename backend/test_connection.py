import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=137.131.246.149;"
    "DATABASE=dtbTransporte;"
    "UID=consulta.pbi;"
    "PWD=Br$Samor@2025#C;"
    "TrustServerCertificate=yes;"
)

try:
    print("Testando conexão com o banco dtbTransporte...")
    conn = pyodbc.connect(conn_str, timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM tbdOcorrenciaNota")
    row = cursor.fetchone()
    if row:
        print("✅ Conexão bem-sucedida! Exemplo de linha:")
        print(row)
    else:
        print("⚠️ Conexão OK, mas nenhuma linha retornada da tabela tbdOcorrenciaNota.")
    conn.close()
except Exception as e:
    print(f"❌ Erro ao conectar ou consultar: {e}") 