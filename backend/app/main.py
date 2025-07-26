from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, sinistros, sinistros_automacao_simple

# REMOVIDO: Base.metadata.create_all(bind=engine) 
# As tabelas já existem nos bancos de dados

app = FastAPI(
    title="Sinistros Control API",
    description="API para controle de sinistros",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # URLs do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# plugando as rotas
app.include_router(auth.router)
app.include_router(sinistros.router)
app.include_router(sinistros_automacao_simple.router)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Sinistros Control API está funcionando",
        "version": "1.0.0"
    }
