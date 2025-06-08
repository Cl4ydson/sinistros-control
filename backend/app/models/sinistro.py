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