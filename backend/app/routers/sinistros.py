from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..database import get_db
from ..models.sinistro import SinistroView
from ..schemas.sinistro import SinistroOut
from ..core.auth import get_current_user

router = APIRouter(prefix="/sinistros", tags=["sinistros"])

@router.get("/", response_model=List[SinistroOut])
def list_sinistros(
    dt_ini: date | None = Query(None, description="Data inicial do filtro"),
    dt_fim: date | None = Query(None, description="Data final do filtro"),
    modal: str | None = Query(None, description="Modal de transporte"),
    cliente: str | None = Query(None, description="Nome do cliente"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        q = db.query(SinistroView)
        
        if dt_ini:
            q = q.filter(SinistroView.data_evento >= dt_ini)
        if dt_fim:
            q = q.filter(SinistroView.data_evento <= dt_fim)
        if modal:
            q = q.filter(SinistroView.modal == modal)
        if cliente:
            q = q.filter(SinistroView.cliente.ilike(f"%{cliente}%"))
            
        return q.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar sinistros"
        )