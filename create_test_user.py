"""
Script para criar usuário de teste
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from app.database import SessionLocal_Principal
from app.models.user import User

def create_test_user():
    """Cria um usuário de teste"""
    
    db = SessionLocal_Principal()
    
    try:
        # Verificar se já existe
        existing_user = db.query(User).filter_by(login="admin").first()
        if existing_user:
            print("✅ Usuário 'admin' já existe")
            return
        
        # Criar usuário
        user = User(
            login="admin",
            email="admin@test.com",
            nome="Administrador"
        )
        user.set_password("admin")
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print("✅ Usuário 'admin' criado com sucesso")
        print(f"   Login: admin")
        print(f"   Senha: admin")
        print(f"   Email: admin@test.com")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
        db.rollback()
        
        # Tentar criar a tabela se não existir
        try:
            from app.database import Base, engine_principal
            Base.metadata.create_all(bind=engine_principal)
            print("✅ Tabelas criadas")
            
            # Tentar novamente
            user = User(
                login="admin",
                email="admin@test.com",
                nome="Administrador"
            )
            user.set_password("admin")
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            print("✅ Usuário 'admin' criado após criar tabelas")
            
        except Exception as e2:
            print(f"❌ Erro mesmo após criar tabelas: {e2}")
            
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()