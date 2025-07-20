"""
Repositório para a tabela eSinistros no banco AUTOMACAO_BRSAMOR
Implementação real com pyodbc para salvar e recuperar dados
"""

import pyodbc
from typing import Optional, Dict, List
from datetime import datetime, date
import logging
import json

logger = logging.getLogger(__name__)

class ESinistrosRepository:
    """Repository para operações na tabela eSinistros"""
    
    def __init__(self):
        # Credenciais do banco AUTOMACAO_BRSAMOR
        self.conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=SRVTOTVS02;"
            "DATABASE=AUTOMACAO_BRSAMOR;"
            "UID=adm;"
            "PWD=(Br$amor#2020);"
            "TrustServerCertificate=yes;"
        )
    
    def _get_connection(self):
        """Cria uma nova conexão"""
        return pyodbc.connect(self.conn_str)
    
    def test_connection(self) -> bool:
        """Testa a conexão com o banco"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            conn.close()
            print("Conexão com AUTOMACAO_BRSAMOR OK")
            return True
        except Exception as e:
            print(f"Erro na conexão com AUTOMACAO_BRSAMOR: {e}")
            return False
    
    def verificar_tabela_existe(self) -> bool:
        """Verifica se a tabela eSinistros existe"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'eSinistros'
            """)
            
            existe = cursor.fetchone()[0] > 0
            conn.close()
            
            print(f"Tabela eSinistros existe: {existe}")
            return existe
            
        except Exception as e:
            logger.error(f"Erro ao verificar tabela: {e}")
            return False
    
    def criar_tabela_se_nao_existe(self):
        """Cria a tabela eSinistros se não existir"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # SQL para criar a tabela com todas as colunas mencionadas
            create_table_sql = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='eSinistros' AND xtype='U')
            CREATE TABLE [dbo].[eSinistros] (
                [ID] [int] IDENTITY(1,1) PRIMARY KEY,
                [Nota Fiscal] [varchar](50) NULL,
                [Minu.Conh] [varchar](50) NULL,
                [Remetente] [varchar](200) NULL,
                [Destinatário] [varchar](200) NULL,
                [Data Coleta] [date] NULL,
                [Prazo Entrega] [date] NULL,
                [Data Entrega] [date] NULL,
                [Ocorrência] [varchar](100) NULL,
                [Compl. Ocorrência] [text] NULL,
                [ULTIMA OCORRENCIA] [varchar](100) NULL,
                [REFERENCIA] [varchar](50) NULL,
                [Data Agendamento] [date] NULL,
                [Data Ocorrência] [date] NULL,
                [Data Cadastro] [date] NULL,
                [Hora Cadastro] [time] NULL,
                [Data Alteração] [date] NULL,
                [Hora Alteração] [time] NULL,
                [Valor Nota Fiscal] [decimal](15,2) NULL,
                [Valor Frete] [decimal](15,2) NULL,
                [Cidade Destino] [varchar](100) NULL,
                [UF Destino] [varchar](2) NULL,
                [PAGAMENTO] [varchar](100) NULL,
                [VENDA] [varchar](100) NULL,
                [a] [varchar](10) NULL,
                [CÓD ] [varchar](20) NULL,
                [MÊS] [int] NULL,
                [ANO] [int] NULL,
                [FILIAL ORIGEM] [varchar](100) NULL,
                [DATA DO SINISTRO] [date] NULL,
                [ND] [varchar](50) NULL,
                [TIPO DO PRODUTO ] [varchar](100) NULL,
                [QNT PRODUTOS] [int] NULL,
                [CLIENTE] [varchar](200) NULL,
                [RESPONSÁVEL PELA AVARIA] [varchar](100) NULL,
                [MODAL] [varchar](50) NULL,
                [TIPO] [varchar](50) NULL,
                [CÓD RNC] [varchar](50) NULL,
                [RNC RETORNADO?] [bit] NULL,
                [DESCRIÇÃO] [text] NULL,
                [STATUS CARGA RETORNO] [varchar](100) NULL,
                [STATUS SINISTRO] [varchar](100) NULL,
                [CIA] [varchar](100) NULL,
                [AWB] [varchar](50) NULL,
                [VALOR DO SINISTRO ] [decimal](15,2) NULL,
                [SALVADOS] [decimal](15,2) NULL,
                [INDENIZADOS] [decimal](15,2) NULL,
                [DEVOLUÇÃO] [decimal](15,2) NULL,
                [USO INTERNO] [decimal](15,2) NULL,
                [SALDO ESTOQUE] [decimal](15,2) NULL,
                [JURIDICO] [decimal](15,2) NULL,
                [SEGURO] [decimal](15,2) NULL,
                [PREJUÍZO] [decimal](15,2) NULL,
                [VALIDAÇÃO] [varchar](100) NULL,
                [DIFERENÇA] [decimal](15,2) NULL,
                [PROGRAMAÇÃO DE PAGAMENTO] [text] NULL,
                [DATA DE PAGAMENTO] [date] NULL,
                [STATUS PAGAMENTO] [varchar](100) NULL,
                [JURÍDICO ACIONADO?] [bit] NULL,
                [SEGURO ACIONADO?] [bit] NULL,
                [PROGRAMAÇÃO INDENIZAÇÃO] [text] NULL,
                [DATA INDENIZAÇÃO] [date] NULL,
                [QUANTIDADE DE PARCELAS INDENIZAÇÃO] [int] NULL,
                [PRIMEIRA PARCELA INDENIZAÇÃO] [date] NULL,
                [ULTIMA PARCELA INDENIZAÇÃO] [date] NULL,
                [JUSTIFICATIVA DE PREJUÍZO BR] [text] NULL,
                [VENDIDO?] [bit] NULL,
                [QUANTIDADE DE PARCELAS DA VENDA] [int] NULL,
                [PRIMEIRA PARCELA DE VENDA] [date] NULL,
                [ULTIMA PARCELA DE VENDA] [date] NULL,
                [DATA DE PAGAMENTO VENDA] [date] NULL,
                [DATA DA ATUALIZAÇÃO SINISTRO] [datetime] NULL,
                [STATUS] [varchar](100) NULL,
                [CONCLUÍDO?] [bit] NULL,
                [CRIADO_EM] [datetime] DEFAULT GETDATE(),
                [CRIADO_POR] [varchar](100) NULL,
                [ATUALIZADO_EM] [datetime] DEFAULT GETDATE(),
                [ATUALIZADO_POR] [varchar](100) NULL
            )
            """
            
            cursor.execute(create_table_sql)
            conn.commit()
            conn.close()
            
            print("Tabela eSinistros criada/verificada com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar tabela: {e}")
            return False
    
    def buscar_por_nota_conhecimento(self, nota_fiscal: str, nr_conhecimento: Optional[str] = None) -> Optional[Dict]:
        """Busca sinistro por nota fiscal e conhecimento"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if nr_conhecimento:
                sql = """
                SELECT * FROM [dbo].[eSinistros] 
                WHERE [Nota Fiscal] = ? AND [Minu.Conh] = ?
                """
                cursor.execute(sql, [nota_fiscal, nr_conhecimento])
            else:
                sql = """
                SELECT * FROM [dbo].[eSinistros] 
                WHERE [Nota Fiscal] = ?
                """
                cursor.execute(sql, [nota_fiscal])
            
            # Obter colunas
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            
            if row:
                # Converter para dicionário
                result = {}
                for i, value in enumerate(row):
                    column_name = columns[i]
                    result[column_name] = value
                
                # Mapear campos para frontend
                result_frontend = self._mapear_campos_para_frontend(result)
                
                conn.close()
                return result_frontend
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar sinistro: {e}")
            return None
    
    def salvar_ou_atualizar(self, dados: Dict) -> bool:
        """Salva ou atualiza sinistro na tabela eSinistros"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            nota_fiscal = dados.get('nota_fiscal') or dados.get('Nota Fiscal')
            nr_conhecimento = dados.get('nr_conhecimento') or dados.get('Minu.Conh')
            
            # Verificar se já existe
            sinistro_existente = self.buscar_por_nota_conhecimento(nota_fiscal, nr_conhecimento)
            
            if sinistro_existente:
                # ATUALIZAR
                return self._atualizar_sinistro(cursor, conn, dados, sinistro_existente['ID'])
            else:
                # CRIAR NOVO
                return self._criar_sinistro(cursor, conn, dados)
                
        except Exception as e:
            logger.error(f"Erro ao salvar/atualizar sinistro: {e}")
            return False
    
    def _criar_sinistro(self, cursor, conn, dados: Dict) -> bool:
        """Cria novo sinistro"""
        try:
            # Mapear campos dos dados recebidos para colunas da tabela
            campos_mapeados = self._mapear_campos(dados)
            
            # Construir SQL de INSERT
            colunas = list(campos_mapeados.keys())
            valores = list(campos_mapeados.values())
            placeholders = ', '.join(['?' for _ in valores])
            colunas_str = ', '.join([f'[{col}]' for col in colunas])
            
            sql = f"""
            INSERT INTO [dbo].[eSinistros] ({colunas_str})
            VALUES ({placeholders})
            """
            
            logger.info(f"Executing SQL: {sql}")
            logger.info(f"With values: {valores}")
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()
            
            logger.info(f"Sinistro criado: {dados.get('nota_fiscal')}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar sinistro: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def _atualizar_sinistro(self, cursor, conn, dados: Dict, sinistro_id: int) -> bool:
        """Atualiza sinistro existente"""
        try:
            # Mapear campos dos dados recebidos para colunas da tabela
            campos_mapeados = self._mapear_campos(dados)
            
            # Construir SQL de UPDATE
            set_clauses = []
            valores = []
            
            for coluna, valor in campos_mapeados.items():
                if valor is not None:  # Só atualizar campos não-nulos
                    set_clauses.append(f'[{coluna}] = ?')
                    valores.append(valor)
            
            if not set_clauses:
                conn.close()
                return True  # Nada para atualizar
            
            valores.append(sinistro_id)
            
            sql = f"""
            UPDATE [dbo].[eSinistros] 
            SET {', '.join(set_clauses)}
            WHERE [ID] = ?
            """
            
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()
            
            logger.info(f"Sinistro atualizado: ID {sinistro_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar sinistro: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def _mapear_campos(self, dados: Dict) -> Dict:
        """Mapeia campos dos dados recebidos para colunas da tabela"""
        # Debug: mostrar dados recebidos
        logger.info(f"Dados recebidos para mapeamento: {dados}")
        
        mapeamento = {
            # Dados básicos
            'nota_fiscal': 'Nota Fiscal',
            'nr_conhecimento': 'Minu.Conh',
            'remetente': 'Remetente',
            'destinatario': 'Destinatário',
            'cliente': 'CLIENTE',
            
            # Datas
            'data_coleta': 'Data Coleta',
            'prazo_entrega': 'Prazo Entrega',
            'data_entrega': 'Data Entrega',
            'data_agendamento': 'Data Agendamento',
            'data_ocorrencia': 'Data Ocorrência',
            'data_cadastro': 'Data Cadastro',
            'hora_cadastro': 'Hora Cadastro',
            'data_alteracao': 'Data Alteração',
            'hora_alteracao': 'Hora Alteração',
            'data_sinistro': 'DATA DO SINISTRO',
            'data_pagamento': 'DATA DE PAGAMENTO',
            'data_indenizacao': 'DATA INDENIZAÇÃO',
            'data_pagamento_venda': 'DATA DE PAGAMENTO VENDA',
            'data_atualizacao_sinistro': 'DATA DA ATUALIZAÇÃO SINISTRO',
            
            # Ocorrências
            'ocorrencia': 'Ocorrência',
            'tipo_ocorrencia': 'Ocorrência',
            'compl_ocorrencia': 'Compl. Ocorrência',
            'descricao_ocorrencia': 'Compl. Ocorrência',
            'ultima_ocorrencia': 'ULTIMA OCORRENCIA',
            'descricao': 'DESCRIÇÃO',
            
            # Referências
            'referencia': 'REFERENCIA',
            'cod': 'CÓD',
            'cod_rnc': 'CÓD RNC',
            'awb': 'AWB',
            'nd': 'ND',
            
            # Valores
            'valor_nota_fiscal': 'Valor Nota Fiscal',
            'valor_frete': 'Valor Frete',
            'valor_sinistro': 'VALOR DO SINISTRO ',
            'valor_indenizacao': 'VALOR DO SINISTRO ',  # Frontend sends valor_indenizacao (note trailing space)
            'valor_liberado': 'USO INTERNO',  # Frontend sends valor_liberado for uso interno
            'valor_salvados_vendido': 'SALVADOS',  # Frontend field mapping
            'valor_venda_salvados': 'DEVOLUÇÃO',  # Frontend field mapping
            'percentual_desconto_salvados': 'DIFERENÇA',  # Frontend field mapping
            'responsavel_compra_salvados': 'CLIENTE',  # Map to cliente field instead
            'salvados': 'SALVADOS',
            'indenizados': 'INDENIZADOS',
            'devolucao': 'DEVOLUÇÃO',
            'uso_interno': 'USO INTERNO',
            'saldo_estoque': 'SALDO ESTOQUE',
            'juridico': 'JURIDICO',
            'seguro': 'SEGURO',
            'prejuizo': 'PREJUÍZO',
            'diferenca': 'DIFERENÇA',
            
            # Localização
            'cidade_destino': 'Cidade Destino',
            'uf_destino': 'UF Destino',
            'filial_origem': 'FILIAL ORIGEM',
            'setor_responsavel': 'FILIAL ORIGEM',  # Map setor to filial field
            
            # Produto
            'tipo_produto': 'TIPO DO PRODUTO ',
            'qnt_produtos': 'QNT PRODUTOS',
            'responsavel_avaria': 'RESPONSÁVEL PELA AVARIA',
            
            # Classificações
            'modal': 'MODAL',
            'tipo': 'TIPO',
            'cia': 'CIA',
            
            # Controles
            'mes': 'MÊS',
            'ano': 'ANO',
            
            # Status
            'pagamento': 'PAGAMENTO',
            'venda': 'VENDA',
            'status_carga_retorno': 'STATUS CARGA RETORNO',
            'status_sinistro': 'STATUS SINISTRO',
            'status_geral': 'STATUS SINISTRO',  # Frontend sends status_geral
            'status_pagamento': 'STATUS PAGAMENTO',
            'status_indenizacao': 'STATUS',  # Map to STATUS column instead
            'status': 'STATUS',
            
            # Campos especiais
            'a': 'a',
            'rnc_retornado': 'RNC RETORNADO?',
            'validacao': 'VALIDAÇÃO',
            'concluido': 'CONCLUÍDO?',
            'vendido': 'VENDIDO?',
            
            # Acionamentos
            'juridico_acionado': 'JURÍDICO ACIONADO?',
            'seguro_acionado': 'SEGURO ACIONADO?',
            
            # Programações
            'programacao_pagamento': 'PROGRAMAÇÃO DE PAGAMENTO',
            'programacao_indenizacao': 'PROGRAMAÇÃO INDENIZAÇÃO',
            'quantidade_parcelas_indenizacao': 'QUANTIDADE DE PARCELAS INDENIZAÇÃO',
            'primeira_parcela_indenizacao': 'PRIMEIRA PARCELA INDENIZAÇÃO',
            'ultima_parcela_indenizacao': 'ULTIMA PARCELA INDENIZAÇÃO',
            'quantidade_parcelas_venda': 'QUANTIDADE DE PARCELAS DA VENDA',
            'primeira_parcela_venda': 'PRIMEIRA PARCELA DE VENDA',
            'ultima_parcela_venda': 'ULTIMA PARCELA DE VENDA',
            
            # Justificativas
            'justificativa_prejuizo': 'JUSTIFICATIVA DE PREJUÍZO BR',
            
            # NEW STANDARDIZED COLUMNS - Payment section
            'numero_nd': 'numero_nd',
            'data_vencimento_nd': 'data_vencimento_nd', 
            'observacoes_pagamento': 'observacoes_pagamento',
            
            # NEW STANDARDIZED COLUMNS - Internal use section
            'observacoes_internas': 'observacoes_internas',
            'responsavel_interno': 'responsavel_interno',
            'data_liberacao': 'data_liberacao',
            'setor_recebimento': 'setor_recebimento',
            
            # NEW STANDARDIZED COLUMNS - Legal section
            'custas_juridicas': 'custas_juridicas',
            'status_juridico': 'status_juridico', 
            'data_abertura_juridico': 'data_abertura_juridico',
            
            # NEW STANDARDIZED COLUMNS - Insurance section
            'nome_seguradora': 'nome_seguradora',
            'status_seguradora': 'status_seguradora',
            'data_abertura_seguradora': 'data_abertura_seguradora',
            'programacao_indenizacao_seguradora': 'programacao_indenizacao_seguradora',
            
            # NEW STANDARDIZED COLUMNS - Salvage section
            'programacao_pagamento_salvados': 'programacao_pagamento_salvados',
            
            # NEW STANDARDIZED COLUMNS - Indemnification
            'indenizado': 'indenizado',
            
            # NEW STANDARDIZED COLUMNS - Additional fields
            'observacoes_gerais': 'observacoes_gerais',
            'numero_sinistro': 'numero_sinistro'
        }
        
        campos_mapeados = {}
        
        for campo_origem, valor in dados.items():
            if campo_origem in mapeamento:
                coluna_destino = mapeamento[campo_origem]
                campos_mapeados[coluna_destino] = valor
            elif campo_origem in mapeamento.values():
                # Campo já está no formato da coluna
                campos_mapeados[campo_origem] = valor
        
        # Debug: mostrar campos mapeados
        logger.info(f"Campos mapeados: {campos_mapeados}")
        return campos_mapeados
    
    def _mapear_campos_para_frontend(self, dados_db: Dict) -> Dict:
        """Mapeia campos do banco de dados para formato esperado pelo frontend"""
        mapeamento_reverso = {
            # Dados básicos
            'Nota Fiscal': 'nota_fiscal',
            'Minu.Conh': 'nr_conhecimento',
            'STATUS SINISTRO': 'status_geral',
            'STATUS PAGAMENTO': 'status_pagamento',
            'STATUS': 'status_indenizacao',
            'VALOR DO SINISTRO ': 'valor_indenizacao',  # Note trailing space
            'USO INTERNO': 'valor_liberado',
            'SALVADOS': 'valor_salvados_vendido',
            'DEVOLUÇÃO': 'valor_venda_salvados',
            'DIFERENÇA': 'percentual_desconto_salvados',
            'RESPONSÁVEL PELA AVARIA': 'responsavel_avaria',
            'FILIAL ORIGEM': 'setor_responsavel',
            'CLIENTE': 'responsavel_compra_salvados',
            'JURIDICO': 'custas_juridicas',
            'JURÍDICO ACIONADO?': 'acionamento_juridico',
            'SEGURO ACIONADO?': 'acionamento_seguradora',
            'DESCRIÇÃO': 'observacoes',
            
            # NEW STANDARDIZED COLUMNS - Reverse mapping
            'numero_nd': 'numero_nd',
            'data_vencimento_nd': 'data_vencimento_nd',
            'observacoes_pagamento': 'observacoes_pagamento',
            'observacoes_internas': 'observacoes_internas',
            'responsavel_interno': 'responsavel_interno',
            'data_liberacao': 'data_liberacao',
            'setor_recebimento': 'setor_recebimento',
            'custas_juridicas': 'custas_juridicas',
            'status_juridico': 'status_juridico',
            'data_abertura_juridico': 'data_abertura_juridico',
            'nome_seguradora': 'nome_seguradora',
            'status_seguradora': 'status_seguradora',
            'data_abertura_seguradora': 'data_abertura_seguradora',
            'programacao_indenizacao_seguradora': 'programacao_indenizacao_seguradora',
            'programacao_pagamento_salvados': 'programacao_pagamento_salvados',
            'indenizado': 'indenizado',
            'observacoes_gerais': 'observacoes_gerais',
            'numero_sinistro': 'numero_sinistro'
        }
        
        campos_frontend = {}
        
        for coluna_db, valor in dados_db.items():
            if coluna_db in mapeamento_reverso:
                campo_frontend = mapeamento_reverso[coluna_db]
                campos_frontend[campo_frontend] = valor
            else:
                # Manter campos que não têm mapeamento
                campos_frontend[coluna_db] = valor
                
        return campos_frontend
    
    def listar_todos(self, limit: int = 100) -> List[Dict]:
        """Lista todos os sinistros da tabela"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = f"SELECT TOP {limit} * FROM [dbo].[eSinistros] ORDER BY [Nota Fiscal] DESC"
            cursor.execute(sql)
            
            # Obter colunas
            columns = [column[0] for column in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                result = {}
                for i, value in enumerate(row):
                    column_name = columns[i]
                    result[column_name] = value
                results.append(result)
            
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Erro ao listar sinistros: {e}")
            return []