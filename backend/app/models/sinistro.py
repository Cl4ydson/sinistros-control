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

class SinistroView(Base):
    """
    View/Model para consulta de sinistros no banco dtbTrans
    Baseado na query fornecida que consulta ocorrências de sinistros
    """
    __tablename__ = "vw_sinistros"  # Será uma view virtual baseada na query
    
    # Campos principais
    nota_fiscal = Column('Nota Fiscal', String(50), primary_key=True)
    nr_conhecimento = Column('Minu.Conh', String(50))
    remetente = Column('Remetente', String(200))
    destinatario = Column('Destinatário', String(200))
    
    # Datas
    dt_coleta = Column('Data Coleta', Date)
    dt_prazo_entrega = Column('Prazo Entrega', Date)
    dt_entrega_real = Column('Data Entrega', Date)
    dt_agendamento = Column('Data Agendamento', Date)
    dt_ocorrencia = Column('Data Ocorrência', Date)
    dt_cadastro = Column('Data Cadastro', Date)
    hr_cadastro = Column('Hora Cadastro', Time)
    dt_alteracao = Column('Data Alteração', Date)
    hr_alteracao = Column('Hora Alteração', Time)
    
    # Ocorrências
    ocorrencia = Column('Ocorrência', String(100))
    compl_ocorrencia = Column('Compl. Ocorrência', String(500))
    ultima_ocorrencia = Column('ULTIMA OCORRENCIA', String(100))
    
    # Referência
    referencia = Column('REFERENCIA', String(50))
    
    # ============================================================
    # NOVOS CAMPOS - STATUS DE PAGAMENTO
    # ============================================================
    status_pagamento = Column(SQLEnum(StatusPagamento), default=StatusPagamento.AGUARDANDO_ND)
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


# Modelo para resposta da API
class SinistroResponse:
    """Modelo de resposta padronizado para sinistros"""
    
    def __init__(self, sinistro_data):
        self.id = f"{sinistro_data.get('nota_fiscal', '')}-{sinistro_data.get('nr_conhecimento', '')}"
        self.nr_conhecimento = sinistro_data.get('nr_conhecimento', '')
        self.nota_fiscal = sinistro_data.get('nota_fiscal', '')
        self.cliente = sinistro_data.get('cliente', '')
        self.remetente = sinistro_data.get('remetente', '')
        self.data_coleta = sinistro_data.get('data_coleta')
        self.prazo_entrega = sinistro_data.get('prazo_entrega')
        self.data_entrega = sinistro_data.get('data_entrega')
        self.data_agendamento = sinistro_data.get('data_agendamento')
        self.data_evento = sinistro_data.get('data_evento')
        self.data_cadastro = sinistro_data.get('data_cadastro')
        self.hora_cadastro = sinistro_data.get('hora_cadastro')
        self.data_alteracao = sinistro_data.get('data_alteracao')
        self.hora_alteracao = sinistro_data.get('hora_alteracao')
        self.modal = sinistro_data.get('modal', 'Rodoviário')
        self.tipo_ocorrencia = sinistro_data.get('tipo_ocorrencia', '')
        self.descricao_ocorrencia = sinistro_data.get('descricao_ocorrencia', '')
        self.ultima_ocorrencia = sinistro_data.get('ultima_ocorrencia', '')
        self.referencia = sinistro_data.get('referencia', '')
        self.status = sinistro_data.get('status', 'Pendente')
        self.valor_mercadoria = float(sinistro_data.get('valor_mercadoria', 0) or 0)
        
    def to_dict(self):
        """Converte para dicionário para serialização JSON"""
        return {
            'id': self.id,
            'nr_conhecimento': self.nr_conhecimento,
            'nota_fiscal': self.nota_fiscal,
            'cliente': self.cliente,
            'remetente': self.remetente,
            'data_coleta': self.data_coleta.isoformat() if self.data_coleta else None,
            'prazo_entrega': self.prazo_entrega.isoformat() if self.prazo_entrega else None,
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'data_agendamento': self.data_agendamento.isoformat() if self.data_agendamento else None,
            'data_evento': self.data_evento.isoformat() if self.data_evento else None,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'hora_cadastro': str(self.hora_cadastro) if self.hora_cadastro else None,
            'data_alteracao': self.data_alteracao.isoformat() if self.data_alteracao else None,
            'hora_alteracao': str(self.hora_alteracao) if self.hora_alteracao else None,
            'modal': self.modal,
            'tipo_ocorrencia': self.tipo_ocorrencia,
            'descricao_ocorrencia': self.descricao_ocorrencia,
            'ultima_ocorrencia': self.ultima_ocorrencia,
            'referencia': self.referencia,
            'status': self.status,
            'valor_mercadoria': self.valor_mercadoria
        }

# ====================================================================
# CLASSE PARA GERENCIAR PROGRAMAÇÃO DE PAGAMENTO
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
    
    def __init__(self, sinistro_data):
        self.sinistro_data = sinistro_data
    
    def to_dict(self) -> Dict:
        """Converte para dicionário completo para API"""
        return {
            # Dados básicos
            "id": self.sinistro_data.get("id"),
            "nota_fiscal": self.sinistro_data.get("nota_fiscal"),
            "nr_conhecimento": self.sinistro_data.get("nr_conhecimento"),
            "remetente": self.sinistro_data.get("remetente"),
            "destinatario": self.sinistro_data.get("destinatario"),
            
            # Status
            "status_pagamento": self.sinistro_data.get("status_pagamento"),
            "status_indenizacao": self.sinistro_data.get("status_indenizacao"),
            "status_juridico": self.sinistro_data.get("status_juridico"),
            "status_seguradora": self.sinistro_data.get("status_seguradora"),
            
            # Valores
            "valor_sinistro_total": float(self.sinistro_data.get("valor_sinistro_total", 0)),
            "valor_indenizado_total": float(self.sinistro_data.get("valor_indenizado_total", 0)),
            "valor_uso_interno": float(self.sinistro_data.get("valor_uso_interno", 0)),
            "valor_seguradora_total": float(self.sinistro_data.get("valor_seguradora_total", 0)),
            "valor_juridico_total": float(self.sinistro_data.get("valor_juridico_total", 0)),
            "valor_salvados": float(self.sinistro_data.get("valor_salvados", 0)),
            
            # Cálculo do prejuízo
            "prejuizo_total": (
                float(self.sinistro_data.get("valor_indenizado_total", 0)) +
                float(self.sinistro_data.get("valor_uso_interno", 0)) +
                float(self.sinistro_data.get("valor_seguradora_total", 0)) +
                float(self.sinistro_data.get("valor_juridico_total", 0)) -
                float(self.sinistro_data.get("valor_salvados", 0))
            ),
            
            # Uso interno
            "setor_responsavel": self.sinistro_data.get("setor_responsavel"),
            "responsavel_interno": self.sinistro_data.get("responsavel_interno"),
            
            # Jurídico
            "numero_processo": self.sinistro_data.get("numero_processo"),
            "escritorio_advocacia": self.sinistro_data.get("escritorio_advocacia"),
            
            # Seguradora
            "nome_seguradora": self.sinistro_data.get("nome_seguradora"),
            "numero_sinistro_seguradora": self.sinistro_data.get("numero_sinistro_seguradora"),
            "dt_programacao_indenizacao": self.sinistro_data.get("dt_programacao_indenizacao"),
            
            # Programação de pagamento
            "programacao_pagamento": self.sinistro_data.get("programacao_pagamento", []),
        }