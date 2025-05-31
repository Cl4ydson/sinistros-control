from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth  # importe seus routers
from .database import engine, Base

# Criar as tabelas (se necessário)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sua API", version="1.0.0")

# Configuração CORS - MUITO IMPORTANTE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:5173", 
        "http://localhost:3000",  # React Create App default
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "API está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)