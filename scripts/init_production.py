#!/usr/bin/env python3
"""
Script para inicializar dados em produção
Deve ser executado após o primeiro deploy no Coolify
"""

import sys
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Configura o banco de dados inicial"""
    try:
        # Adicionar o diretório da aplicação ao path
        app_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
        if app_path not in sys.path:
            sys.path.insert(0, app_path)
        
        from app.database import get_db_principal
        from app.models.user import User
        from app.repositories.sinistros_controle_repository import SinistrosControleRepository
        
        logger.info("🔧 Inicializando banco de dados...")
        
        # Testar conexão
        db = next(get_db_principal())
        logger.info("✅ Conexão com banco principal OK")
        
        # Verificar se já existe usuário admin
        existing_admin = db.query(User).filter_by(login="admin").first()
        if not existing_admin:
            # Criar usuário admin
            admin_user = User(
                nome="Administrador do Sistema",
                login="admin",
                email="admin@brsamor.com.br",
                setor="TI"
            )
            admin_user.set_password("BrSamor@2025!")  # Senha forte para produção
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            logger.info("✅ Usuário admin criado com sucesso")
            logger.info("   Login: admin")
            logger.info("   Senha: BrSamor@2025!")
        else:
            logger.info("✅ Usuário admin já existe")
        
        # Verificar/criar tabelas de sinistros
        repo = SinistrosControleRepository()
        if repo.test_connection():
            logger.info("✅ Conexão com repositório de sinistros OK")
            repo.criar_tabelas_se_nao_existem()
            logger.info("✅ Tabelas de sinistros verificadas/criadas")
        else:
            logger.error("❌ Falha na conexão com repositório de sinistros")
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao configurar banco: {str(e)}")
        return False

def verify_environment():
    """Verifica se as variáveis de ambiente estão configuradas"""
    required_vars = [
        'DB_SERVER', 'DB_DATABASE', 'DB_USERNAME', 'DB_PASSWORD',
        'DB_TRANSPORT_SERVER', 'DB_TRANSPORT_DATABASE', 
        'DB_TRANSPORT_USERNAME', 'DB_TRANSPORT_PASSWORD',
        'SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error("❌ Variáveis de ambiente faltando:")
        for var in missing_vars:
            logger.error(f"   - {var}")
        return False
    
    logger.info("✅ Todas as variáveis de ambiente estão configuradas")
    return True

def main():
    """Função principal"""
    logger.info("🚀 Inicializando sistema em produção...")
    
    # Verificar variáveis de ambiente
    if not verify_environment():
        logger.error("⚠️  Configure as variáveis de ambiente no Coolify")
        return 1
    
    # Configurar banco de dados
    if not setup_database():
        logger.error("⚠️  Falha na configuração do banco de dados")
        return 1
    
    logger.info("🎉 Sistema inicializado com sucesso!")
    logger.info("📱 Acesse a aplicação através do domínio configurado")
    logger.info("🔐 Use as credenciais: admin / BrSamor@2025!")
    
    return 0

if __name__ == "__main__":
    exit(main())