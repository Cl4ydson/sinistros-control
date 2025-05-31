import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ========== BANCO PRINCIPAL (AUTOMACAO_BRSAMOR) ==========
# Credenciais para banco principal - usuários, auth, etc.
user_principal = "adm"
password_principal = "(Br$amor#2020)"
server_principal = "SRVTOTVS02"
database_principal = "AUTOMACAO_BRSAMOR"

params_principal = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server_principal};DATABASE={database_principal};"
    f"UID={user_principal};PWD={password_principal}"
)

SQLALCHEMY_DATABASE_URL_PRINCIPAL = f"mssql+pyodbc:///?odbc_connect={params_principal}"

# Engine e Session para banco principal
engine_principal = create_engine(SQLALCHEMY_DATABASE_URL_PRINCIPAL)
SessionLocal_Principal = sessionmaker(bind=engine_principal, autocommit=False, autoflush=False)

# ========== BANCO SINISTRO (AUTOMACAO) ==========
# Credenciais para banco de sinistros
user_sinistro = "consulta.pbi"
password_sinistro = "naMf.}T3KVg+3fo6Z7Sq"
server_sinistro = "172.30.0.211"
database_sinistro = "dtbTransporte"

# Usar connection string direta que funciona
conn_str_sinistro = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_sinistro};DATABASE={database_sinistro};UID={user_sinistro};PWD={password_sinistro};TrustServerCertificate=yes;"
SQLALCHEMY_DATABASE_URL_SINISTRO = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str_sinistro)}"

# Engine e Session para banco sinistro
engine_sinistro = create_engine(SQLALCHEMY_DATABASE_URL_SINISTRO)
SessionLocal_Sinistro = sessionmaker(bind=engine_sinistro, autocommit=False, autoflush=False)

# ========== BASE DECLARATIVA ==========
Base = declarative_base()

# ========== DEPENDENCY FUNCTIONS ==========
def get_db_principal():
    """Dependency para obter sessão do banco principal"""
    db = SessionLocal_Principal()
    try:
        yield db
    finally:
        db.close()

def get_db_sinistro():
    """Dependency para obter sessão do banco de sinistros"""
    db = SessionLocal_Sinistro()
    try:
        yield db
    finally:
        db.close()

# Manter compatibilidade com código existente
get_db = get_db_principal
engine = engine_principal