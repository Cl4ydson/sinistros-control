from fastapi import APIRouter, HTTPException
from ..demo_data import DEMO_SINISTROS
from typing import List, Dict, Any

router = APIRouter(
    prefix="/api/automacao",
    tags=["sinistros-demo"]
)

@router.get("/sinistros")
def get_sinistros_demo(skip: int = 0, limit: int = 100):
    """Lista sinistros em modo demonstração"""
    total = len(DEMO_SINISTROS)
    sinistros = DEMO_SINISTROS[skip:skip + limit]
    
    return {
        "success": True,
        "data": sinistros,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "pages": (total + limit - 1) // limit if limit > 0 else 1
    }

@router.get("/sinistros/{sinistro_id}")
def get_sinistro_demo(sinistro_id: int):
    """Obtém um sinistro específico em modo demo"""
    for sinistro in DEMO_SINISTROS:
        if sinistro["id"] == sinistro_id:
            return {
                "success": True,
                "data": sinistro
            }
    
    raise HTTPException(status_code=404, detail="Sinistro não encontrado")

@router.get("/dashboard/stats/{periodo}")
def get_dashboard_stats_demo(periodo: int = 30):
    """Estatísticas do dashboard em modo demo"""
    return {
        "success": True,
        "data": {
            "total_sinistros": len(DEMO_SINISTROS),
            "valor_total": sum(s["valor"] for s in DEMO_SINISTROS),
            "em_analise": len([s for s in DEMO_SINISTROS if s["status"] == "Em Análise"]),
            "aprovados": len([s for s in DEMO_SINISTROS if s["status"] == "Aprovado"]),
            "rejeitados": len([s for s in DEMO_SINISTROS if s["status"] == "Rejeitado"]),
            "periodo": periodo
        }
    }

@router.get("/dashboard/recentes")
def get_sinistros_recentes_demo():
    """Sinistros recentes em modo demo"""
    return {
        "success": True,
        "data": DEMO_SINISTROS[:5]  # Últimos 5
    }