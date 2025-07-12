from sqlalchemy import Column, Integer, String, DateTime, Numeric, Date, Time, Text, Enum as SQLEnum, JSON
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from decimal import Decimal
from typing import Dict, List, Optional
from datetime import date, datetime

Base = declarative_base()

# ====================================================================
# ENUMS PARA STATUS - ABORDAGEM ULTRATHINK
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
# MODELO PRINCIPAL EXPANDIDO - SINISTRO COMPLETO
# ====================================================================

class SinistroCompleto(Base):
    """
    Modelo completo de sinistro com todos os campos solicitados
    Abordagem ULTRATHINK: Estrutura escalável e modular
    """
    __tablename__ = "sinistros_completos"
    
    # ============================================================
    # CAMPOS PRIMÁRIOS (EXISTENTES)
    # ============================================================
    id = Column(Integer, primary_key=True, index=True)
    nota_fiscal = Column(String(50), index=True)
    nr_conhecimento = Column(String(50), index=True)
    remetente = Column(String(200))
    destinatario = Column(String(200))
    
    # Datas originais
    dt_coleta = Column(Date)
    dt_prazo_entrega = Column(Date)
    dt_entrega_real = Column(Date)
    dt_agendamento = Column(Date)
    dt_ocorrencia = Column(Date)
    dt_cadastro = Column(Date)
    hr_cadastro = Column(Time)
    dt_alteracao = Column(Date)
    hr_alteracao = Column(Time)
    
    # Ocorrências originais
    ocorrencia = Column(String(100))
    compl_ocorrencia = Column(Text)
    ultima_ocorrencia = Column(String(100))
    referencia = Column(String(50))
    
    # ============================================================
    # NOVOS CAMPOS - STATUS DE PAGAMENTO
    # ============================================================
    status_pagamento = Column(SQLEnum(StatusPagamento), default=StatusPagamento.PENDENTE)
    observacoes_pagamento = Column(Text)
    dt_status_pagamento = Column(DateTime, default=datetime.utcnow)
    
    # ============================================================
    # NOVOS CAMPOS - STATUS DE INDENIZAÇÃO
    # ============================================================
    status_indenizacao = Column(SQLEnum(StatusIndenizacao), default=StatusIndenizacao.PENDENTE)
    valor_indenizacao = Column(Numeric(15, 2), default=0)
    observacoes_indenizacao = Column(Text)
    dt_status_indenizacao = Column(DateTime, default=datetime.utcnow)
    
    # ============================================================
    # INDENIZADOS - PROGRAMAÇÃO DE PAGAMENTO
    # ============================================================
    programacao_pagamento = Column(JSON)  # Até 10 datas de pagamento
    tipo_documento_esl = Column(SQLEnum(TipoDocumento))
    numero_documento_esl = Column(String(100))
    valor_documento_esl = Column(Numeric(15, 2))
    dt_vencimento_documento = Column(Date)
    
    # ============================================================
    # USO INTERNO
    # ============================================================
    setor_responsavel = Column(String(100))
    responsavel_interno = Column(String(100))
    observacoes_internas = Column(Text)
    dt_ultima_atualizacao_interna = Column(DateTime, default=datetime.utcnow)
    
    # ============================================================
    # JURÍDICO
    # ============================================================
    status_juridico = Column(SQLEnum(StatusJuridico))
    numero_processo = Column(String(100))
    escritorio_advocacia = Column(String(200))
    valor_causa_juridica = Column(Numeric(15, 2))
    dt_abertura_juridico = Column(Date)
    dt_status_juridico = Column(DateTime, default=datetime.utcnow)
    observacoes_juridico = Column(Text)
    
    # ============================================================
    # SEGURADORA
    # ============================================================
    status_seguradora = Column(SQLEnum(StatusSeguradora))
    nome_seguradora = Column(String(200))
    numero_sinistro_seguradora = Column(String(100))
    valor_cobertura = Column(Numeric(15, 2))
    dt_abertura_seguradora = Column(Date)
    dt_programacao_indenizacao = Column(Date)
    dt_status_seguradora = Column(DateTime, default=datetime.utcnow)
    observacoes_seguradora = Column(Text)
    
    # ============================================================
    # CAMPO FINAL - VALORES CONSOLIDADOS (PREJUÍZO)
    # ============================================================
    valor_sinistro_total = Column(Numeric(15, 2), default=0)
    valor_indenizado_total = Column(Numeric(15, 2), default=0)
    valor_uso_interno = Column(Numeric(15, 2), default=0)
    valor_seguradora_total = Column(Numeric(15, 2), default=0)
    valor_juridico_total = Column(Numeric(15, 2), default=0)
    valor_salvados = Column(Numeric(15, 2), default=0)
    
    # Cálculo automático do prejuízo
    @property
    def prejuizo_total(self) -> Decimal:
        """
        Calcula o prejuízo total: 
        (Indenizados + Uso Interno + Seguradora + Jurídico) - Salvados
        """
        return (
            (self.valor_indenizado_total or 0) +
            (self.valor_uso_interno or 0) +
            (self.valor_seguradora_total or 0) +
            (self.valor_juridico_total or 0) -
            (self.valor_salvados or 0)
        )
    
    # ============================================================
    # CAMPOS DE AUDITORIA
    # ============================================================
    criado_em = Column(DateTime, default=datetime.utcnow)
    criado_por = Column(String(100))
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    atualizado_por = Column(String(100))

# ====================================================================
# MODELO DE PROGRAMAÇÃO DE PAGAMENTO
# ====================================================================

class ProgramacaoPagamento:
    """
    Estrutura para programação de pagamento (até 10 datas)
    Armazenado como JSON no campo programacao_pagamento
    """
    
    def __init__(self):
        self.pagamentos: List[Dict] = []
    
    def adicionar_pagamento(self, data: date, valor: Decimal, descricao: str = ""):
        """Adiciona um pagamento programado (máximo 10)"""
        if len(self.pagamentos) >= 10:
            raise ValueError("Máximo de 10 programações de pagamento permitidas")
        
        self.pagamentos.append({
            "data": data.isoformat(),
            "valor": float(valor),
            "descricao": descricao,
            "pago": False,
            "dt_pagamento": None
        })
    
    def marcar_como_pago(self, indice: int, dt_pagamento: date):
        """Marca um pagamento como realizado"""
        if 0 <= indice < len(self.pagamentos):
            self.pagamentos[indice]["pago"] = True
            self.pagamentos[indice]["dt_pagamento"] = dt_pagamento.isoformat()
    
    def to_dict(self) -> Dict:
        """Converte para dicionário para armazenamento JSON"""
        return {"pagamentos": self.pagamentos}
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProgramacaoPagamento':
        """Cria instância a partir de dicionário"""
        instance = cls()
        instance.pagamentos = data.get("pagamentos", [])
        return instance

# ====================================================================
# CLASSE DE RESPOSTA COMPLETA PARA API
# ====================================================================

class SinistroCompletoResponse:
    """
    Classe de resposta completa para API
    Abordagem ULTRATHINK: Serialização otimizada
    """
    
    def __init__(self, sinistro: SinistroCompleto):
        self.sinistro = sinistro
    
    def to_dict(self) -> Dict:
        """Converte para dicionário completo para API"""
        return {
            # Dados básicos
            "id": self.sinistro.id,
            "nota_fiscal": self.sinistro.nota_fiscal,
            "nr_conhecimento": self.sinistro.nr_conhecimento,
            "remetente": self.sinistro.remetente,
            "destinatario": self.sinistro.destinatario,
            
            # Datas
            "dt_coleta": self.sinistro.dt_coleta.isoformat() if self.sinistro.dt_coleta else None,
            "dt_ocorrencia": self.sinistro.dt_ocorrencia.isoformat() if self.sinistro.dt_ocorrencia else None,
            
            # Status
            "status_pagamento": self.sinistro.status_pagamento.value if self.sinistro.status_pagamento else None,
            "status_indenizacao": self.sinistro.status_indenizacao.value if self.sinistro.status_indenizacao else None,
            "status_juridico": self.sinistro.status_juridico.value if self.sinistro.status_juridico else None,
            "status_seguradora": self.sinistro.status_seguradora.value if self.sinistro.status_seguradora else None,
            
            # Valores
            "valor_sinistro_total": float(self.sinistro.valor_sinistro_total or 0),
            "valor_indenizado_total": float(self.sinistro.valor_indenizado_total or 0),
            "valor_uso_interno": float(self.sinistro.valor_uso_interno or 0),
            "valor_seguradora_total": float(self.sinistro.valor_seguradora_total or 0),
            "valor_juridico_total": float(self.sinistro.valor_juridico_total or 0),
            "valor_salvados": float(self.sinistro.valor_salvados or 0),
            "prejuizo_total": float(self.sinistro.prejuizo_total),
            
            # Programação de pagamento
            "programacao_pagamento": self.sinistro.programacao_pagamento,
            
            # Uso interno
            "setor_responsavel": self.sinistro.setor_responsavel,
            "responsavel_interno": self.sinistro.responsavel_interno,
            
            # Jurídico
            "numero_processo": self.sinistro.numero_processo,
            "escritorio_advocacia": self.sinistro.escritorio_advocacia,
            
            # Seguradora
            "nome_seguradora": self.sinistro.nome_seguradora,
            "numero_sinistro_seguradora": self.sinistro.numero_sinistro_seguradora,
            "dt_programacao_indenizacao": self.sinistro.dt_programacao_indenizacao.isoformat() if self.sinistro.dt_programacao_indenizacao else None,
            
            # Auditoria
            "criado_em": self.sinistro.criado_em.isoformat() if self.sinistro.criado_em else None,
            "atualizado_em": self.sinistro.atualizado_em.isoformat() if self.sinistro.atualizado_em else None,
        } 