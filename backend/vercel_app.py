"""
Adaptador para deploy no Vercel
Este arquivo configura a aplicação FastAPI para funcionar como serverless function
"""

from app.main import app

# Handler para Vercel
def handler(event, context):
    """
    Handler principal para Vercel serverless functions
    """
    return app(event, context)

# Para desenvolvimento local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 