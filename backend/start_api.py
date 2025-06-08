#!/usr/bin/env python3
"""
Script para iniciar a API
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Iniciando API de Sinistros...")
    print("📍 URL: http://127.0.0.1:8001")
    print("📖 Docs: http://127.0.0.1:8001/docs")
    print("=" * 50)
    
    try:
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8001, 
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Erro ao iniciar API: {e}")
        import traceback
        traceback.print_exc() 