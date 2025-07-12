from sqlalchemy import Column, Integer, String, DateTime, Numeric, Date, Time, Text, Boolean
from datetime import datetime
from ..database import Base

class SinistroAutomacao(Base):
    """
    Modelo para mapear a tabela eSinistros do banco AUTOMACAO_BRSAMOR
    Mapeamento direto dos campos reais da tabela existente
    """
    __tablename__ = "eSinistros"
    
    # Chave primária (assumindo que existe um ID)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Mapeamento dos campos da tabela eSinistros
    nota_fiscal = Column("Nota Fiscal", String(100))
    nr_conhecimento = Column("Minu.Conh", String(100))
    remetente = Column("Remetente", String(200))
    destinatario = Column("Destinatário", String(200))
    
    # Datas
    dt_coleta = Column("Data Coleta", Date)
    dt_prazo_entrega = Column("Prazo Entrega", Date)
    dt_entrega = Column("Data Entrega", Date)
    dt_agendamento = Column("Data Agendamento", Date)
    dt_ocorrencia = Column("Data Ocorrência", Date)
    dt_cadastro = Column("Data Cadastro", Date)
    hr_cadastro = Column("Hora Cadastro", Time)
    dt_alteracao = Column("Data Alteração", Date)
    hr_alteracao = Column("Hora Alteração", Time)
    
    # Ocorrências
    ocorrencia = Column("Ocorrência", String(100))
    compl_ocorrencia = Column("Compl. Ocorrência", Text)
    ultima_ocorrencia = Column("ULTIMA OCORRENCIA", String(100))
    referencia = Column("REFERENCIA", String(100))
    
    # Valores
    valor_nota_fiscal = Column("Valor Nota Fiscal", Numeric(15, 2))
    valor_frete = Column("Valor Frete", Numeric(15, 2))
    
    # Localização
    cidade_destino = Column("Cidade Destino", String(100))
    uf_destino = Column("UF Destino", String(2))
    
    # Campos específicos do negócio
    pagamento = Column("PAGAMENTO", String(100))
    venda = Column("VENDA", String(100))
    a = Column("a", String(100))  # Campo específico da tabela
    cod = Column("CÓD ", String(50))
    mes = Column("MÊS", String(20))
    ano = Column("ANO", String(10))
    filial_origem = Column("FILIAL ORIGEM", String(100))
    
    # Data do sinistro
    dt_sinistro = Column("DATA DO SINISTRO", Date)
    nd = Column("ND", String(100))
    tipo_produto = Column("TIPO DO PRODUTO ", String(100))
    qnt_produtos = Column("QNT PRODUTOS", Integer)
    cliente = Column("CLIENTE", String(200))
    responsavel_avaria = Column("RESPONSÁVEL PELA AVARIA", String(200))
    modal = Column("MODAL", String(50))
    tipo = Column("TIPO", String(100))
    
    # RNC
    cod_rnc = Column("CÓD RNC", String(100))
    rnc_retornado = Column("RNC RETORNADO?", String(20))
    descricao = Column("DESCRIÇÃO", Text)
    status_carga_retorno = Column("STATUS CARGA RETORNO", String(100))
    status_sinistro = Column("STATUS SINISTRO", String(100))
    
    # Seguradora/Transportes
    cia = Column("CIA", String(100))
    awb = Column("AWB", String(100))
    
    # Valores financeiros
    valor_sinistro = Column("VALOR DO SINISTRO ", Numeric(15, 2))
    salvados = Column("SALVADOS", Numeric(15, 2))
    indenizados = Column("INDENIZADOS", Numeric(15, 2))
    devolucao = Column("DEVOLUÇÃO", Numeric(15, 2))
    uso_interno = Column("USO INTERNO", Numeric(15, 2))
    saldo_estoque = Column("SALDO ESTOQUE", Numeric(15, 2))
    juridico = Column("JURIDICO", Numeric(15, 2))
    seguro = Column("SEGURO", Numeric(15, 2))
    prejuizo = Column("PREJUÍZO", Numeric(15, 2))
    validacao = Column("VALIDAÇÃO", Numeric(15, 2))
    diferenca = Column("DIFERENÇA", Numeric(15, 2))
    
    # Pagamentos e programação
    programacao_pagamento = Column("PROGRAMAÇÃO DE PAGAMENTO", String(200))
    dt_pagamento = Column("DATA DE PAGAMENTO", Date)
    status_pagamento = Column("STATUS PAGAMENTO", String(100))
    
    # Acionamentos
    juridico_acionado = Column("JURÍDICO ACIONADO?", String(20))
    seguro_acionado = Column("SEGURO ACIONADO?", String(20))
    
    # Indenização
    programacao_indenizacao = Column("PROGRAMAÇÃO INDENIZAÇÃO", String(200))
    dt_indenizacao = Column("DATA INDENIZAÇÃO", Date)
    qnt_parcelas_indenizacao = Column("QUANTIDADE DE PARCELAS INDENIZAÇÃO", Integer)
    primeira_parcela_indenizacao = Column("PRIMEIRA PARCELA INDENIZAÇÃO", Date)
    ultima_parcela_indenizacao = Column("ULTIMA PARCELA INDENIZAÇÃO", Date)
    justificativa_prejuizo = Column("JUSTIFICATIVA DE PREJUÍZO BR", Text)
    
    # Venda
    vendido = Column("VENDIDO?", String(20))
    qnt_parcelas_venda = Column("QUANTIDADE DE PARCELAS DA VENDA", Integer)
    primeira_parcela_venda = Column("PRIMEIRA PARCELA DE VENDA", Date)
    ultima_parcela_venda = Column("ULTIMA PARCELA DE VENDA", Date)
    dt_pagamento_venda = Column("DATA DE PAGAMENTO VENDA", Date)
    
    # Status e controle
    dt_atualizacao_sinistro = Column("DATA DA ATUALIZAÇÃO SINISTRO", DateTime)
    status = Column("STATUS", String(100))
    concluido = Column("CONCLUÍDO?", String(20))
    
    # Campos de auditoria (podem não existir na tabela original)
    criado_em = Column(DateTime, default=datetime.utcnow)
    criado_por = Column(String(100))
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    atualizado_por = Column(String(100))

    def to_dict(self):
        """Converte para dicionário para compatibilidade com a API"""
        return {
            'id': self.id,
            'nota': self.nota_fiscal,
            'numero': self.nr_conhecimento,
            'remetente': self.remetente,
            'destinatario': self.destinatario,
            'status': self.status or self.status_sinistro,
            'dt_coleta': self.dt_coleta.isoformat() if self.dt_coleta is not None else None,
            'dt_entrega': self.dt_entrega.isoformat() if self.dt_entrega is not None else None,
            'ocorrencia': self.ocorrencia,
            'descricao': self.descricao,
            'valor_sinistro': float(str(self.valor_sinistro)) if self.valor_sinistro is not None else None,
            'cliente': self.cliente,
            'modal': self.modal,
            'cidade_destino': self.cidade_destino,
            'uf_destino': self.uf_destino
        } 