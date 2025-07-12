from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict
from enum import Enum

# ====================================================================
# ENUMS PARA VALIDAÇÃO - ABORDAGEM ULTRATHINK
# ====================================================================

class StatusPagamento(str, Enum):
    """Status dos pagamentos relacionados ao sinistro"""
    AGUARDANDO_ND = "Aguardando ND"
    AGUARDANDO_PAGAMENTO = "Aguardando Pagamento"
    PAGO = "Pago"
    EM_TRATATIVA = "Em tratativa"

class StatusIndenizacao(str, Enum):
    """Status das indenizações"""
    PROGRAMADO = "Programado"
    PAGO = "Pago"
    PENDENTE = "Pendente"
    PAGO_PARCIAL = "Pago Parcial"

class StatusJuridico(str, Enum):
    """Status do processo jurídico"""
    AGUARDANDO_ABERTURA = "Aguardando abertura"
    PROCESSO_INICIADO = "Processo iniciado"
    INDENIZADO = "Indenizado"

class StatusSeguradora(str, Enum):
    """Status do processo com seguradora"""
    AGUARDANDO_ABERTURA = "Aguardando abertura"
    PROCESSO_INICIADO = "Processo iniciado"
    INDENIZADO = "Indenizado"

class TipoDocumento(str, Enum):
    """Tipos de documentos ESL"""
    BOLETO = "Boleto"
    TITULO = "Título"
    OUTROS = "Outros"

# ====================================================================
# SCHEMAS DE ENTRADA E SAÍDA - ESCALÁVEIS
# ====================================================================

class ProgramacaoPagamentoItem(BaseModel):
    """Item individual de programação de pagamento"""
    data: date = Field(..., description="Data do pagamento programado")
    valor: Decimal = Field(..., description="Valor do pagamento", ge=0)
    descricao: str = Field("", description="Descrição do pagamento")
    pago: bool = Field(False, description="Se foi pago ou não")
    dt_pagamento: Optional[date] = Field(None, description="Data que foi efetivamente pago")

class SinistroBase(BaseModel):
    """Schema base do sinistro com campos básicos"""
    nota_fiscal: str = Field(..., max_length=50, description="Número da nota fiscal")
    nr_conhecimento: Optional[str] = Field(None, max_length=50, description="Número do conhecimento")
    remetente: Optional[str] = Field(None, max_length=200, description="Nome do remetente")
    destinatario: Optional[str] = Field(None, max_length=200, description="Nome do destinatário")

class SinistroCreate(SinistroBase):
    """Schema para criação de sinistro"""
    # Campos opcionais para criação
    dt_coleta: Optional[date] = None
    dt_ocorrencia: Optional[date] = None
    ocorrencia: Optional[str] = Field(None, max_length=100)
    compl_ocorrencia: Optional[str] = None
    
    # Novos campos para criação
    setor_responsavel: Optional[str] = Field(None, max_length=100, description="Setor responsável")
    responsavel_interno: Optional[str] = Field(None, max_length=100, description="Responsável interno")
    
class SinistroUpdate(BaseModel):
    """Schema para atualização de sinistro - todos os campos opcionais"""
    
    # ============================================================
    # CAMPOS DE PAGAMENTO
    # ============================================================
    status_pagamento: Optional[StatusPagamento] = None
    observacoes_pagamento: Optional[str] = None
    
    # ============================================================
    # CAMPOS DE INDENIZAÇÃO
    # ============================================================
    status_indenizacao: Optional[StatusIndenizacao] = None
    valor_indenizacao: Optional[Decimal] = Field(None, ge=0)
    observacoes_indenizacao: Optional[str] = None
    
    # ============================================================
    # PROGRAMAÇÃO DE PAGAMENTO
    # ============================================================
    programacao_pagamento: Optional[List[ProgramacaoPagamentoItem]] = Field(
        None, max_items=10, description="Até 10 programações de pagamento"
    )
    tipo_documento_esl: Optional[TipoDocumento] = None
    numero_documento_esl: Optional[str] = Field(None, max_length=100)
    valor_documento_esl: Optional[Decimal] = Field(None, ge=0)
    dt_vencimento_documento: Optional[date] = None
    
    # ============================================================
    # USO INTERNO
    # ============================================================
    setor_responsavel: Optional[str] = Field(None, max_length=100)
    responsavel_interno: Optional[str] = Field(None, max_length=100)
    observacoes_internas: Optional[str] = None
    
    # ============================================================
    # JURÍDICO
    # ============================================================
    status_juridico: Optional[StatusJuridico] = None
    numero_processo: Optional[str] = Field(None, max_length=100)
    escritorio_advocacia: Optional[str] = Field(None, max_length=200)
    valor_causa_juridica: Optional[Decimal] = Field(None, ge=0)
    dt_abertura_juridico: Optional[date] = None
    observacoes_juridico: Optional[str] = None
    
    # ============================================================
    # SEGURADORA
    # ============================================================
    status_seguradora: Optional[StatusSeguradora] = None
    nome_seguradora: Optional[str] = Field(None, max_length=200)
    numero_sinistro_seguradora: Optional[str] = Field(None, max_length=100)
    valor_cobertura: Optional[Decimal] = Field(None, ge=0)
    dt_abertura_seguradora: Optional[date] = None
    dt_programacao_indenizacao: Optional[date] = None
    observacoes_seguradora: Optional[str] = None
    
    # ============================================================
    # VALORES CONSOLIDADOS
    # ============================================================
    valor_sinistro_total: Optional[Decimal] = Field(None, ge=0, description="Valor total do sinistro")
    valor_indenizado_total: Optional[Decimal] = Field(None, ge=0, description="Total indenizado")
    valor_uso_interno: Optional[Decimal] = Field(None, ge=0, description="Valor uso interno")
    valor_seguradora_total: Optional[Decimal] = Field(None, ge=0, description="Valor seguradora")
    valor_juridico_total: Optional[Decimal] = Field(None, ge=0, description="Valor jurídico")
    valor_salvados: Optional[Decimal] = Field(None, ge=0, description="Valor dos salvados")

class SinistroOut(SinistroBase):
    """Schema de saída completo do sinistro"""
    id: int
    
    # Datas
    dt_coleta: Optional[date] = None
    dt_prazo_entrega: Optional[date] = None
    dt_entrega_real: Optional[date] = None
    dt_agendamento: Optional[date] = None
    dt_ocorrencia: Optional[date] = None
    dt_cadastro: Optional[date] = None
    hr_cadastro: Optional[str] = None
    dt_alteracao: Optional[date] = None
    hr_alteracao: Optional[str] = None
    
    # Ocorrências
    ocorrencia: Optional[str] = None
    compl_ocorrencia: Optional[str] = None
    ultima_ocorrencia: Optional[str] = None
    referencia: Optional[str] = None
    
    # ============================================================
    # NOVOS CAMPOS DE SAÍDA
    # ============================================================
    
    # Status
    status_pagamento: Optional[StatusPagamento] = None
    status_indenizacao: Optional[StatusIndenizacao] = None
    status_juridico: Optional[StatusJuridico] = None
    status_seguradora: Optional[StatusSeguradora] = None
    
    # Valores
    valor_sinistro_total: Optional[Decimal] = Field(0, description="Valor total do sinistro")
    valor_indenizado_total: Optional[Decimal] = Field(0, description="Total indenizado")
    valor_uso_interno: Optional[Decimal] = Field(0, description="Valor uso interno")
    valor_seguradora_total: Optional[Decimal] = Field(0, description="Valor seguradora")
    valor_juridico_total: Optional[Decimal] = Field(0, description="Valor jurídico")
    valor_salvados: Optional[Decimal] = Field(0, description="Valor dos salvados")
    prejuizo_total: Optional[Decimal] = Field(0, description="Prejuízo total calculado")
    
    # Uso interno
    setor_responsavel: Optional[str] = None
    responsavel_interno: Optional[str] = None
    observacoes_internas: Optional[str] = None
    
    # Jurídico
    numero_processo: Optional[str] = None
    escritorio_advocacia: Optional[str] = None
    valor_causa_juridica: Optional[Decimal] = None
    dt_abertura_juridico: Optional[date] = None
    observacoes_juridico: Optional[str] = None
    
    # Seguradora
    nome_seguradora: Optional[str] = None
    numero_sinistro_seguradora: Optional[str] = None
    valor_cobertura: Optional[Decimal] = None
    dt_abertura_seguradora: Optional[date] = None
    dt_programacao_indenizacao: Optional[date] = None
    observacoes_seguradora: Optional[str] = None
    
    # Indenização
    valor_indenizacao: Optional[Decimal] = None
    observacoes_indenizacao: Optional[str] = None
    
    # Documento ESL
    tipo_documento_esl: Optional[TipoDocumento] = None
    numero_documento_esl: Optional[str] = None
    valor_documento_esl: Optional[Decimal] = None
    dt_vencimento_documento: Optional[date] = None
    
    # Programação de pagamento
    programacao_pagamento: Optional[List[Dict]] = Field([], description="Lista de pagamentos programados")
    
    # Auditoria
    criado_em: Optional[datetime] = None
    criado_por: Optional[str] = None
    atualizado_em: Optional[datetime] = None
    atualizado_por: Optional[str] = None

    class Config:
        orm_mode = True
        json_encoders = {
            Decimal: float,
            date: lambda v: v.isoformat() if v else None,
            datetime: lambda v: v.isoformat() if v else None
        }

# ====================================================================
# SCHEMAS PARA OPERAÇÕES ESPECÍFICAS
# ====================================================================

class SinistroResumo(BaseModel):
    """Schema resumido para listagens"""
    id: int
    nota_fiscal: str
    nr_conhecimento: Optional[str]
    remetente: Optional[str]
    dt_ocorrencia: Optional[date]
    status_pagamento: Optional[StatusPagamento]
    status_indenizacao: Optional[StatusIndenizacao]
    valor_sinistro_total: Optional[Decimal] = 0
    prejuizo_total: Optional[Decimal] = 0
    setor_responsavel: Optional[str]

class ProgramacaoPagamentoUpdate(BaseModel):
    """Schema para atualizar programação de pagamento"""
    programacao_pagamento: List[ProgramacaoPagamentoItem] = Field(
        ..., max_items=10, description="Até 10 programações de pagamento"
    )

class ValoresConsolidados(BaseModel):
    """Schema para valores consolidados"""
    valor_sinistro_total: Decimal = Field(0, ge=0)
    valor_indenizado_total: Decimal = Field(0, ge=0)
    valor_uso_interno: Decimal = Field(0, ge=0)
    valor_seguradora_total: Decimal = Field(0, ge=0)
    valor_juridico_total: Decimal = Field(0, ge=0)
    valor_salvados: Decimal = Field(0, ge=0)
    
    @property
    def prejuizo_total(self) -> Decimal:
        """Calcula o prejuízo total automaticamente"""
        return (
            self.valor_indenizado_total +
            self.valor_uso_interno +
            self.valor_seguradora_total +
            self.valor_juridico_total -
            self.valor_salvados
        )

# ====================================================================
# SCHEMAS DE RESPOSTA DA API
# ====================================================================

class SinistroResponse(BaseModel):
    """Schema de resposta padrão da API"""
    success: bool = True
    message: str
    data: Optional[SinistroOut] = None

class SinistroListResponse(BaseModel):
    """Schema de resposta para lista de sinistros"""
    success: bool = True
    message: str
    data: Dict = Field(..., description="Contém 'items', 'total', 'page', 'limit'")

class EstatisticasResponse(BaseModel):
    """Schema para estatísticas de sinistros"""
    success: bool = True
    message: str
    data: Dict = Field(..., description="Estatísticas consolidadas")