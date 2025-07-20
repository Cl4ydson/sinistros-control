from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class ProgramacaoPagamento(Base):
    """Modelo para tabela ProgramacaoPagamento no banco AUTOMACAO_BRSAMOR"""
    __tablename__ = "ProgramacaoPagamento"
    
    # Chave primária
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Chave estrangeira para SinistrosControle
    sinistro_id = Column(Integer, ForeignKey('SinistrosControle.id'), nullable=False, index=True)
    
    # Dados do pagamento
    data_pagamento = Column(String(20))  # formato YYYY-MM-DD
    valor_pagamento = Column(Float, default=0.0)
    documento_esl = Column(String(100))  # Número do documento/boleto/título
    
    # Campos de controle
    ordem = Column(Integer, default=1)  # ordem na sequência de pagamentos (1-10)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com sinistro
    sinistro = relationship("SinistroAutomacao", back_populates="programacao_pagamentos", lazy="select")
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            "id": self.id,
            "sinistro_id": self.sinistro_id,
            "data": self.data_pagamento,
            "valor": str(self.valor_pagamento) if self.valor_pagamento else "",
            "doctoESL": self.documento_esl or "",
            "ordem": self.ordem,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }