from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class SinistroAutomacao(Base):
    """Modelo para tabela SinistrosControle no banco AUTOMACAO_BRSAMOR"""
    __tablename__ = "SinistrosControle"
    
    # Chave primária
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Dados básicos
    nota_fiscal = Column(String(50), index=True)
    numero_sinistro = Column(String(50), index=True)
    status_geral = Column(String(50), default="Não iniciado")
    
    # Dados de pagamento
    status_pagamento = Column(String(50), default="Aguardando ND")
    numero_nd = Column(String(50))
    data_vencimento_nd = Column(String(20))  # formato ISO string
    observacoes_pagamento = Column(Text)
    
    # Dados de indenização
    status_indenizacao = Column(String(50), default="Pendente")
    valor_indenizacao = Column(Float, default=0.0)
    responsavel_avaria = Column(String(100))
    indenizado = Column(Boolean, default=False)
    
    # Salvados
    valor_salvados_vendido = Column(Float, default=0.0)
    responsavel_compra_salvados = Column(String(100))
    valor_venda_salvados = Column(Float, default=0.0)
    percentual_desconto_salvados = Column(Float, default=0.0)
    programacao_pagamento_salvados = Column(Text)
    
    # Uso interno
    setor_responsavel = Column(String(100))
    responsavel_interno = Column(String(100))
    data_liberacao = Column(String(20))  # formato ISO string
    valor_liberado = Column(Float, default=0.0)
    observacoes_internas = Column(Text)
    
    # Jurídico
    acionamento_juridico = Column(Boolean, default=False)
    status_juridico = Column(String(50), default="Não acionado")
    data_abertura_juridico = Column(String(20))  # formato ISO string
    custas_juridicas = Column(Float, default=0.0)
    
    # Seguradora
    acionamento_seguradora = Column(Boolean, default=False)
    status_seguradora = Column(String(50), default="Não acionado")
    nome_seguradora = Column(String(100))
    data_abertura_seguradora = Column(String(20))  # formato ISO string
    programacao_indenizacao_seguradora = Column(String(20))  # formato ISO string
    
    # Campos de controle
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_criacao = Column(String(100), default="sistema")
    usuario_atualizacao = Column(String(100), default="sistema")
    
    # Relacionamento com programação de pagamento
    programacao_pagamentos = relationship("ProgramacaoPagamento", back_populates="sinistro", cascade="all, delete-orphan", lazy="select")
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            "id": self.id,
            "nota_fiscal": self.nota_fiscal,
            "numero_sinistro": self.numero_sinistro,
            "status_geral": self.status_geral,
            "status_pagamento": self.status_pagamento,
            "numero_nd": self.numero_nd,
            "data_vencimento_nd": self.data_vencimento_nd,
            "observacoes_pagamento": self.observacoes_pagamento,
            "status_indenizacao": self.status_indenizacao,
            "valor_indenizacao": self.valor_indenizacao,
            "responsavel_avaria": self.responsavel_avaria,
            "indenizado": self.indenizado,
            "valor_salvados_vendido": self.valor_salvados_vendido,
            "responsavel_compra_salvados": self.responsavel_compra_salvados,
            "valor_venda_salvados": self.valor_venda_salvados,
            "percentual_desconto_salvados": self.percentual_desconto_salvados,
            "programacao_pagamento_salvados": self.programacao_pagamento_salvados,
            "setor_responsavel": self.setor_responsavel,
            "responsavel_interno": self.responsavel_interno,
            "data_liberacao": self.data_liberacao,
            "valor_liberado": self.valor_liberado,
            "observacoes_internas": self.observacoes_internas,
            "acionamento_juridico": self.acionamento_juridico,
            "status_juridico": self.status_juridico,
            "data_abertura_juridico": self.data_abertura_juridico,
            "custas_juridicas": self.custas_juridicas,
            "acionamento_seguradora": self.acionamento_seguradora,
            "status_seguradora": self.status_seguradora,
            "nome_seguradora": self.nome_seguradora,
            "data_abertura_seguradora": self.data_abertura_seguradora,
            "programacao_indenizacao_seguradora": self.programacao_indenizacao_seguradora,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            "usuario_criacao": self.usuario_criacao,
            "usuario_atualizacao": self.usuario_atualizacao,
            "programacao_pagamento": [pagamento.to_dict() for pagamento in self.programacao_pagamentos] if hasattr(self, 'programacao_pagamentos') and self.programacao_pagamentos else []
        }