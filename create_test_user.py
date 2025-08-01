#!/usr/bin/env python3
"""
Script para criar um usuário de teste no sistema
"""

import sys
import os

# Adicionar o diretório backend ao path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.database import get_db_principal
from app.models.user import User

def create_test_user():
    """Cria um usuário de teste"""
    print("🔧 Criando usuário de teste...")
    
    try:
        # Obter sessão do banco
        db = next(get_db_principal())
        
        # Verificar se já existe
        existing_user = db.query(User).filter_by(login="admin").first()
        if existing_user:
            print("✅ Usuário 'admin' já existe")
            print(f"   Nome: {existing_user.nome}")
            print(f"   Email: {existing_user.email}")
            print(f"   Setor: {existing_user.setor}")
            return True
        
        # Criar novo usuário
        test_user = User(
            nome="Administrador",
            login="admin",
            email="admin@brsamor.com.br",
            setor="TI"
        )
        test_user.set_password("admin123")
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Usuário de teste criado com sucesso!")
        print(f"   Login: admin")
        print(f"   Senha: admin123")
        print(f"   Nome: {test_user.nome}")
        print(f"   Email: {test_user.email}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🚀 Criando usuário de teste...\n")
    
    success = create_test_user()
    
    if success:
        print("\n🎉 Usuário criado! Agora você pode fazer login com:")
        print("   Login: admin")
        print("   Senha: admin123")
        return 0
    else:
        print("\n⚠️  Falha ao criar usuário.")
        return 1

if __name__ == "__main__":
    exit(main())