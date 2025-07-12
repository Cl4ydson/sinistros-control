from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum

# Enums para padronizar valores
class StatusPagamento(str, Enum):
    AGUARDANDO_ND = "Aguardando ND"
    AGUARDANDO_PAGAMENTO = "Aguardando Pagamento"
    PAGO = "Pago"
    EM_TRATATIVA = "Em tratativa"

class StatusIndenizacao(str, Enum):
    PROGRAMADO = "Programado"
    PAGO = "Pago"
    PENDENTE = "Pendente"
    PAGO_PARCIAL = "Pago Parcial"

class StatusJuridico(str, Enum):
    AGUARDANDO_ABERTURA = "Aguardando abertura"
    PROCESSO_INICIADO = "Processo iniciado"
    INDENIZADO = "Indenizado"

class StatusSeguradora(str, Enum):
    AGUARDANDO_ABERTURA = "Aguardando abertura"
    PROCESSO_INICIADO = "Processo iniciado"
    INDENIZADO = "Indenizado"

class StatusGeral(str, Enum):
    NAO_INICIADO = "Não iniciado"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDO = "Concluído"

# Schema base para criação
class SinistroAutomacaoCreate(BaseModel):
    nota_fiscal: Optional[str] = None
    nr_conhecimento: Optional[str] = None
    remetente: Optional[str] = None
    destinatario: Optional[str] = None
    
    # Datas
    dt_coleta: Optional[date] = None
    dt_prazo_entrega: Optional[date] = None
    dt_entrega: Optional[date] = None
    dt_agendamento: Optional[date] = None
    dt_ocorrencia: Optional[date] = None
    dt_cadastro: Optional[date] = None
    hr_cadastro: Optional[time] = None
    dt_alteracao: Optional[date] = None
    hr_alteracao: Optional[time] = None
    
    # Ocorrências
    ocorrencia: Optional[str] = None
    compl_ocorrencia: Optional[str] = None
    ultima_ocorrencia: Optional[str] = None
    referencia: Optional[str] = None
    
    # Valores
    valor_nota_fiscal: Optional[Decimal] = None
    valor_frete: Optional[Decimal] = None
    
    # Localização
    cidade_destino: Optional[str] = None
    uf_destino: Optional[str] = None
    
    # Campos específicos
    cliente: Optional[str] = None
    modal: Optional[str] = None
    tipo: Optional[str] = None
    
    class Config:
        from_attributes = True

# Schema para atualização
class SinistroAutomacaoUpdate(BaseModel):
    # Campos que podem ser editados pelo usuário
    descricao: Optional[str] = None
    status_sinistro: Optional[str] = None
    
    # Valores financeiros
    valor_sinistro: Optional[Decimal] = None
    salvados: Optional[Decimal] = None
    indenizados: Optional[Decimal] = None
    devolucao: Optional[Decimal] = None
    uso_interno: Optional[Decimal] = None
    juridico: Optional[Decimal] = None
    seguro: Optional[Decimal] = None
    prejuizo: Optional[Decimal] = None
    
    # Status e acionamentos
    status_pagamento: Optional[str] = None
    juridico_acionado: Optional[str] = None
    seguro_acionado: Optional[str] = None
    
    # Programações
    programacao_pagamento: Optional[str] = None
    dt_pagamento: Optional[date] = None
    programacao_indenizacao: Optional[str] = None
    dt_indenizacao: Optional[date] = None
    
    # Status geral
    status: Optional[str] = None
    concluido: Optional[str] = None
    
    class Config:
        from_attributes = True

# Schema para resposta
class SinistroAutomacaoResponse(BaseModel):
    id: int
    nota_fiscal: Optional[str] = None
    nr_conhecimento: Optional[str] = None
    remetente: Optional[str] = None
    destinatario: Optional[str] = None
    cliente: Optional[str] = None
    
    # Datas principais
    dt_coleta: Optional[date] = None
    dt_entrega: Optional[date] = None
    dt_sinistro: Optional[date] = None
    
    # Ocorrências
    ocorrencia: Optional[str] = None
    descricao: Optional[str] = None
    status_sinistro: Optional[str] = None
    
    # Valores
    valor_sinistro: Optional[Decimal] = None
    valor_nota_fiscal: Optional[Decimal] = None
    
    # Localização
    cidade_destino: Optional[str] = None
    uf_destino: Optional[str] = None
    modal: Optional[str] = None
    
    # Status
    status: Optional[str] = None
    concluido: Optional[str] = None
    
    # Auditoria
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema simplificado para listagem
class SinistroAutomacaoList(BaseModel):
    id: int
    nota_fiscal: Optional[str] = None
    nr_conhecimento: Optional[str] = None
    cliente: Optional[str] = None
    status_sinistro: Optional[str] = None
    valor_sinistro: Optional[Decimal] = None
    dt_coleta: Optional[date] = None
    
    class Config:
        from_attributes = True

# Schema para filtros de busca
class SinistroAutomacaoFilter(BaseModel):
    nota_fiscal: Optional[str] = None
    cliente: Optional[str] = None
    status: Optional[str] = None
    dt_inicio: Optional[date] = None
    dt_fim: Optional[date] = None
    modal: Optional[str] = None
    
    class Config:
        from_attributes = True 