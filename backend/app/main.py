from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, sinistros  # importando ambos os routers
from .database import engine, Base

# Criar as tabelas (se necessário)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestão de Sinistros", 
    version="1.0.0",
    description="API para gestão e controle de sinistros de transporte"
)

# Configuração CORS - MUITO IMPORTANTE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:5174",  # Vite default
        "http://127.0.0.1:5173", 
        "http://localhost:3000",  # React Create App default
        "http://127.0.0.1:3000",
        "http://localhost:8001",  # Para o frontend na porta 8001 se houver
        "http://127.0.0.1:8001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(sinistros.router)

@app.get("/")
def read_root():
    return {
        "message": "API de Gestão de Sinistros está funcionando!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API funcionando corretamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)