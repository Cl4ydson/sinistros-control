import urllib.parse
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ========== BANCO PRINCIPAL (AUTOMACAO_BRSAMOR) ==========
# Credenciais para banco principal - usuários, auth, etc.
user_principal = os.getenv("DB_USERNAME", "adm")
password_principal = os.getenv("DB_PASSWORD", "(Br$amor#2020)")
server_principal = os.getenv("DB_SERVER", "SRVTOTVS02")
database_principal = os.getenv("DB_DATABASE", "AUTOMACAO_BRSAMOR")

# Tentar diferentes drivers ODBC em ordem de preferência
drivers_to_try = [
    "ODBC Driver 18 for SQL Server",
    "ODBC Driver 17 for SQL Server", 
    "SQL Server"
]

def get_working_driver():
    """Encontra o primeiro driver ODBC disponível"""
    import pyodbc
    available_drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
    
    for driver in drivers_to_try:
        if driver in available_drivers:
            return driver
    
    # Fallback para o primeiro driver SQL Server disponível
    if available_drivers:
        return available_drivers[0]
    
    # Último recurso
    return "SQL Server"

# Usar driver dinâmico
odbc_driver = get_working_driver()

params_principal = urllib.parse.quote_plus(
    f"DRIVER={{{odbc_driver}}};"
    f"SERVER={server_principal};DATABASE={database_principal};"
    f"UID={user_principal};PWD={password_principal};"
    f"TrustServerCertificate=yes;Encrypt=no;"
)

SQLALCHEMY_DATABASE_URL_PRINCIPAL = f"mssql+pyodbc:///?odbc_connect={params_principal}"

# Engine e Session para banco principal
engine_principal = create_engine(SQLALCHEMY_DATABASE_URL_PRINCIPAL)
SessionLocal_Principal = sessionmaker(bind=engine_principal, autocommit=False, autoflush=False)

# ========== BANCO SINISTRO (AUTOMACAO) ==========
# Credenciais para banco de sinistros
user_sinistro = os.getenv("DB_TRANSPORT_USERNAME", "consulta.pbi")
password_sinistro = os.getenv("DB_TRANSPORT_PASSWORD", "Br$Samor@2025#C")
server_sinistro = os.getenv("DB_TRANSPORT_SERVER", "137.131.246.149")
database_sinistro = os.getenv("DB_TRANSPORT_DATABASE", "dtbTransporte")

# Usar connection string direta que funciona
conn_str_sinistro = f"DRIVER={{{odbc_driver}}};SERVER={server_sinistro};DATABASE={database_sinistro};UID={user_sinistro};PWD={password_sinistro};TrustServerCertificate=yes;Encrypt=no;"
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