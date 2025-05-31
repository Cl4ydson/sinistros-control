from sqlalchemy import Column, Integer, String, DateTime, Numeric, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

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


# Modelo para resposta da API
class SinistroResponse:
    """Modelo de resposta padronizado para sinistros"""
    
    def __init__(self, sinistro_data):
        self.id = f"{sinistro_data.get('Nota Fiscal', '')}-{sinistro_data.get('Minu.Conh', '')}"
        self.nr_conhecimento = sinistro_data.get('Minu.Conh', '')
        self.nota_fiscal = sinistro_data.get('Nota Fiscal', '')
        self.cliente = sinistro_data.get('Destinatário', '')  # Usando destinatário como cliente
        self.remetente = sinistro_data.get('Remetente', '')
        self.data_evento = sinistro_data.get('Data Ocorrência')
        self.data_coleta = sinistro_data.get('Data Coleta')
        self.data_cadastro = sinistro_data.get('Data Cadastro')
        self.hora_cadastro = sinistro_data.get('Hora Cadastro')
        self.data_alteracao = sinistro_data.get('Data Alteração')
        self.hora_alteracao = sinistro_data.get('Hora Alteração')
        self.modal = self._determinar_modal()
        self.tipo_ocorrencia = sinistro_data.get('Ocorrência', '')
        self.descricao_ocorrencia = sinistro_data.get('Compl. Ocorrência', '')
        self.ultima_ocorrencia = sinistro_data.get('ULTIMA OCORRENCIA', '')
        self.referencia = sinistro_data.get('REFERENCIA', '')
        self.status = self._determinar_status()
        self.valor_mercadoria = 0.0  # Não temos este campo na query atual
        
    def _determinar_modal(self):
        """Determina o modal baseado em regras de negócio"""
        # Aqui você pode implementar lógica para determinar o modal
        # baseado no número do conhecimento ou outras informações
        return "Rodoviário"  # Default
        
    def _determinar_status(self):
        """Determina o status baseado na ocorrência"""
        ocorrencia = self.tipo_ocorrencia.upper()
        
        if any(palavra in ocorrencia for palavra in ['AVARIA', 'EXTRAVIO', 'ROUBO', 'SINISTRADA']):
            return "Em análise"
        else:
            return "Pendente"
    
    def to_dict(self):
        """Converte para dicionário para serialização JSON"""
        return {
            'id': self.id,
            'nr_conhecimento': self.nr_conhecimento,
            'nota_fiscal': self.nota_fiscal,
            'cliente': self.cliente,
            'remetente': self.remetente,
            'data_evento': self.data_evento.isoformat() if self.data_evento else None,
            'data_coleta': self.data_coleta.isoformat() if self.data_coleta else None,
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