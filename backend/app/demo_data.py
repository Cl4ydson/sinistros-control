# Dados de demonstração para quando o banco não estiver disponível

DEMO_USERS = [
    {
        "id": 1,
        "login": "admin",
        "email": "admin@brsamor.com.br",
        "nome": "Administrador",
        "senha_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # secret
    },
    {
        "id": 2,
        "login": "user",
        "email": "user@brsamor.com.br", 
        "nome": "Usuário Demo",
        "senha_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # secret
    }
]

DEMO_SINISTROS = [
    {
        "id": 1,
        "nota_fiscal": "12345",
        "conhecimento": "CTR001",
        "cliente": "Cliente Demo 1",
        "valor": 15000.00,
        "status": "Em Análise",
        "data_ocorrencia": "2025-01-15",
        "descricao": "Sinistro de demonstração 1"
    },
    {
        "id": 2,
        "nota_fiscal": "12346", 
        "conhecimento": "CTR002",
        "cliente": "Cliente Demo 2",
        "valor": 25000.00,
        "status": "Aprovado",
        "data_ocorrencia": "2025-01-20",
        "descricao": "Sinistro de demonstração 2"
    },
    {
        "id": 3,
        "nota_fiscal": "12347",
        "conhecimento": "CTR003", 
        "cliente": "Cliente Demo 3",
        "valor": 8500.00,
        "status": "Rejeitado",
        "data_ocorrencia": "2025-01-25",
        "descricao": "Sinistro de demonstração 3"
    }
]

def verify_demo_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica senha para usuários demo"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def get_demo_user_by_login(login: str):
    """Busca usuário demo por login"""
    for user in DEMO_USERS:
        if user["login"] == login:
            return user
    return None