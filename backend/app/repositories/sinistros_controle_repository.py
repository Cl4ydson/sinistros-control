"""
Repositório para as tabelas SinistrosControle e ProgramacaoPagamento no banco AUTOMACAO_BRSAMOR
Implementação real com pyodbc para salvar e recuperar dados
"""

import pyodbc
from typing import Optional, Dict, List
from datetime import datetime, date
import logging
import json

logger = logging.getLogger(__name__)

class SinistrosControleRepository:
    """Repository para operações nas tabelas SinistrosControle e ProgramacaoPagamento"""
    
    def __init__(self):
        # Obter credenciais do ambiente
        import os
        server = os.getenv("DB_SERVER", "SRVTOTVS02")
        database = os.getenv("DB_DATABASE", "AUTOMACAO_BRSAMOR")
        username = os.getenv("DB_USERNAME", "adm")
        password = os.getenv("DB_PASSWORD", "(Br$amor#2020)")
        
        # Tentar diferentes drivers ODBC
        drivers_to_try = [
            "ODBC Driver 18 for SQL Server",
            "ODBC Driver 17 for SQL Server", 
            "SQL Server"
        ]
        
        # Encontrar driver disponível
        available_drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
        odbc_driver = "SQL Server"  # fallback
        
        for driver in drivers_to_try:
            if driver in available_drivers:
                odbc_driver = driver
                break
        
        # Credenciais do banco AUTOMACAO_BRSAMOR
        self.conn_str = (
            f"DRIVER={{{odbc_driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
            f"Encrypt=no;"
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
    
    def verificar_tabelas_existem(self) -> bool:
        """Verifica se as tabelas SinistrosControle e ProgramacaoPagamento existem"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verificar SinistrosControle
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'SinistrosControle'
            """)
            sinistros_existe = cursor.fetchone()[0] > 0
            
            # Verificar ProgramacaoPagamento
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'ProgramacaoPagamento'
            """)
            pagamento_existe = cursor.fetchone()[0] > 0
            
            conn.close()
            
            print(f"Tabela SinistrosControle existe: {sinistros_existe}")
            print(f"Tabela ProgramacaoPagamento existe: {pagamento_existe}")
            return sinistros_existe and pagamento_existe
            
        except Exception as e:
            logger.error(f"Erro ao verificar tabelas: {e}")
            return False
    
    def criar_tabelas_se_nao_existem(self):
        """Cria as tabelas SinistrosControle e ProgramacaoPagamento se não existirem"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # SQL para criar a tabela SinistrosControle
            create_sinistros_sql = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='SinistrosControle' AND xtype='U')
            CREATE TABLE [dbo].[SinistrosControle] (
                [id] [int] IDENTITY(1,1) PRIMARY KEY,
                [nota_fiscal] [varchar](50) NULL,
                [numero_sinistro] [varchar](50) NULL,
                [status_geral] [varchar](100) NULL,
                [status_pagamento] [varchar](100) NULL,
                [numero_nd] [varchar](50) NULL,
                [data_vencimento_nd] [date] NULL,
                [observacoes_pagamento] [text] NULL,
                [status_indenizacao] [varchar](100) NULL,
                [valor_indenizacao] [decimal](15,2) NULL,
                [responsavel_avaria] [varchar](200) NULL,
                [indenizado] [bit] NULL,
                [valor_salvados_vendido] [decimal](15,2) NULL,
                [responsavel_compra_salvados] [varchar](200) NULL,
                [valor_venda_salvados] [decimal](15,2) NULL,
                [percentual_desconto_salvados] [decimal](5,2) NULL,
                [programacao_pagamento_salvados] [text] NULL,
                [setor_responsavel] [varchar](100) NULL,
                [responsavel_interno] [varchar](200) NULL,
                [data_liberacao] [date] NULL,
                [valor_liberado] [decimal](15,2) NULL,
                [observacoes_internas] [text] NULL,
                [acionamento_juridico] [bit] NULL,
                [status_juridico] [varchar](100) NULL,
                [data_abertura_juridico] [date] NULL,
                [custas_juridicas] [decimal](15,2) NULL,
                [acionamento_seguradora] [bit] NULL,
                [status_seguradora] [varchar](100) NULL,
                [nome_seguradora] [varchar](200) NULL,
                [data_abertura_seguradora] [date] NULL,
                [programacao_indenizacao_seguradora] [text] NULL,
                [data_criacao] [datetime] DEFAULT GETDATE(),
                [data_atualizacao] [datetime] DEFAULT GETDATE(),
                [usuario_criacao] [varchar](100) NULL,
                [usuario_atualizacao] [varchar](100) NULL
            )
            """
            
            # SQL para criar a tabela ProgramacaoPagamento
            create_pagamento_sql = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ProgramacaoPagamento' AND xtype='U')
            CREATE TABLE [dbo].[ProgramacaoPagamento] (
                [id] [int] IDENTITY(1,1) PRIMARY KEY,
                [sinistro_id] [int] NOT NULL,
                [data_pagamento] [date] NULL,
                [valor_pagamento] [decimal](15,2) NULL,
                [documento_esl] [varchar](100) NULL,
                [ordem] [int] NULL,
                [data_criacao] [datetime] DEFAULT GETDATE(),
                [data_atualizacao] [datetime] DEFAULT GETDATE(),
                FOREIGN KEY ([sinistro_id]) REFERENCES [dbo].[SinistrosControle]([id])
            )
            """
            
            cursor.execute(create_sinistros_sql)
            cursor.execute(create_pagamento_sql)
            conn.commit()
            conn.close()
            
            print("Tabelas SinistrosControle e ProgramacaoPagamento criadas/verificadas com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            return False
    
    def buscar_por_nota_fiscal(self, nota_fiscal: str) -> Optional[Dict]:
        """Busca sinistro por nota fiscal incluindo programação de pagamento"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Buscar dados principais do sinistro
            sql = """
            SELECT * FROM [dbo].[SinistrosControle] 
            WHERE [nota_fiscal] = ?
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
                
                sinistro_id = result.get('id')
                
                # Buscar programação de pagamento se existir sinistro_id
                if sinistro_id:
                    programacao = self._buscar_programacao_pagamento(sinistro_id)
                    result['programacao_pagamento'] = programacao
                else:
                    result['programacao_pagamento'] = []
                
                conn.close()
                return result
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar sinistro: {e}")
            return None
    
    def _buscar_programacao_pagamento(self, sinistro_id: int) -> List[Dict]:
        """Busca programação de pagamento para um sinistro específico"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Debug: verificar se existe o sinistro_id
            logger.info(f"Buscando programação para sinistro_id: {sinistro_id}")
            
            sql = """
            SELECT [data_pagamento], [valor_pagamento], [documento_esl], [ordem]
            FROM [dbo].[ProgramacaoPagamento] 
            WHERE [sinistro_id] = ?
            ORDER BY [ordem]
            """
            cursor.execute(sql, [sinistro_id])
            
            registros = cursor.fetchall()
            programacao = []
            
            logger.info(f"Encontrados {len(registros)} registros na tabela ProgramacaoPagamento para sinistro_id {sinistro_id}")
            
            for registro in registros:
                data_pag, valor_pag, doc_esl, ordem = registro
                
                # Converter data para string no formato correto
                data_formatada = ''
                if data_pag:
                    if hasattr(data_pag, 'strftime'):
                        # É um objeto date/datetime
                        data_formatada = data_pag.strftime('%Y-%m-%d')
                    else:
                        # É uma string, usar diretamente
                        data_formatada = str(data_pag)
                
                # Converter para o formato esperado pelo frontend
                item = {
                    "data": data_formatada,
                    "valor": str(valor_pag) if valor_pag else '',
                    "doctoESL": doc_esl if doc_esl else ''
                }
                programacao.append(item)
                logger.info(f"Item programação: {item}")
            
            conn.close()
            
            # Se não há programação, retornar pelo menos um item vazio para o frontend
            if not programacao:
                programacao = [{"data": "", "valor": "", "doctoESL": ""}]
                logger.info("Nenhuma programação encontrada, retornando item vazio")
            
            return programacao
            
        except Exception as e:
            logger.error(f"Erro ao buscar programação de pagamento: {e}")
            return [{"data": "", "valor": "", "doctoESL": ""}]
    
    def salvar_ou_atualizar(self, dados: Dict) -> bool:
        """Salva ou atualiza sinistro na tabela SinistrosControle"""
        try:
            nota_fiscal = dados.get('nota_fiscal')
            if not nota_fiscal:
                logger.error("Nota fiscal é obrigatória")
                return False
            
            logger.info(f"Salvando/atualizando sinistro: NF={nota_fiscal}")
            
            # Verificar se já existe
            sinistro_existente = self.buscar_por_nota_fiscal(nota_fiscal)
            
            if sinistro_existente and sinistro_existente.get('id'):
                # ATUALIZAR
                logger.info(f"Atualizando sinistro existente ID: {sinistro_existente['id']}")
                return self._atualizar_sinistro(dados, sinistro_existente['id'])
            else:
                # CRIAR NOVO
                logger.info("Criando novo sinistro")
                return self._criar_sinistro(dados)
                
        except Exception as e:
            logger.error(f"Erro ao salvar/atualizar sinistro: {e}")
            return False
    
    def _criar_sinistro(self, dados: Dict) -> bool:
        """Cria novo sinistro"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Mapear campos dos dados recebidos para colunas da tabela
            campos_mapeados = self._mapear_campos_sinistros(dados)
            
            # Construir SQL de INSERT
            colunas = list(campos_mapeados.keys())
            valores = list(campos_mapeados.values())
            placeholders = ', '.join(['?' for _ in valores])
            colunas_str = ', '.join([f'[{col}]' for col in colunas])
            
            sql = f"""
            INSERT INTO [dbo].[SinistrosControle] ({colunas_str})
            VALUES ({placeholders})
            """
            
            logger.info(f"Executing SQL: {sql}")
            logger.info(f"With values: {valores}")
            cursor.execute(sql, valores)
            conn.commit()
            
            # Obter o ID do sinistro criado
            cursor.execute("SELECT @@IDENTITY")
            sinistro_id = cursor.fetchone()[0]
            
            conn.close()
            
            logger.info(f"Sinistro criado com ID: {sinistro_id}")
            
            # Se há dados de pagamento, salvar na tabela de programação
            if self._tem_dados_pagamento(dados):
                self._salvar_programacao_pagamento(sinistro_id, dados)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar sinistro: {e}")
            return False
    
    def _atualizar_sinistro(self, dados: Dict, sinistro_id: int) -> bool:
        """Atualiza sinistro existente"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Mapear campos dos dados recebidos para colunas da tabela
            campos_mapeados = self._mapear_campos_sinistros(dados)
            
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
            
            # Adicionar data de atualização
            set_clauses.append('[data_atualizacao] = GETDATE()')
            valores.append(sinistro_id)
            
            sql = f"""
            UPDATE [dbo].[SinistrosControle] 
            SET {', '.join(set_clauses)}
            WHERE [id] = ?
            """
            
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()
            
            logger.info(f"Sinistro atualizado: ID {sinistro_id}")
            
            # Se há dados de pagamento, atualizar na tabela de programação
            if self._tem_dados_pagamento(dados):
                self._atualizar_programacao_pagamento(sinistro_id, dados)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar sinistro: {e}")
            return False
    
    def _mapear_campos_sinistros(self, dados: Dict) -> Dict:
        """Mapeia campos dos dados recebidos para colunas da tabela SinistrosControle"""
        # Validar e converter tipos de dados
        dados_validados = self._validar_tipos(dados)
        
        mapeamento = {
            # Dados básicos
            'nota_fiscal': 'nota_fiscal',
            'numero_sinistro': 'numero_sinistro',
            'status_geral': 'status_geral',
            'status_sinistro': 'status_geral',  # Alias
            'status_pagamento': 'status_pagamento',
            'numero_nd': 'numero_nd',
            'data_vencimento_nd': 'data_vencimento_nd',
            'observacoes_pagamento': 'observacoes_pagamento',
            
            # Indenização
            'status_indenizacao': 'status_indenizacao',
            'valor_indenizacao': 'valor_indenizacao',
            'valor_sinistro': 'valor_indenizacao',  # Alias
            'responsavel_avaria': 'responsavel_avaria',
            'indenizado': 'indenizado',
            
            # Salvados
            'valor_salvados_vendido': 'valor_salvados_vendido',
            'responsavel_compra_salvados': 'responsavel_compra_salvados',
            'valor_venda_salvados': 'valor_venda_salvados',
            'percentual_desconto_salvados': 'percentual_desconto_salvados',
            'programacao_pagamento_salvados': 'programacao_pagamento_salvados',
            
            # Interno
            'setor_responsavel': 'setor_responsavel',
            'responsavel_interno': 'responsavel_interno',
            'data_liberacao': 'data_liberacao',
            'valor_liberado': 'valor_liberado',
            'observacoes_internas': 'observacoes_internas',
            
            # Jurídico
            'acionamento_juridico': 'acionamento_juridico',
            'juridico_acionado': 'acionamento_juridico',  # Alias
            'status_juridico': 'status_juridico',
            'data_abertura_juridico': 'data_abertura_juridico',
            'custas_juridicas': 'custas_juridicas',
            
            # Seguradora
            'acionamento_seguradora': 'acionamento_seguradora',
            'seguro_acionado': 'acionamento_seguradora',  # Alias
            'status_seguradora': 'status_seguradora',
            'nome_seguradora': 'nome_seguradora',
            'data_abertura_seguradora': 'data_abertura_seguradora',
            'programacao_indenizacao_seguradora': 'programacao_indenizacao_seguradora',
            
            # Usuário
            'usuario_criacao': 'usuario_criacao',
            'usuario_atualizacao': 'usuario_atualizacao'
        }
        
        campos_mapeados = {}
        
        for campo_origem, valor in dados_validados.items():
            if campo_origem in mapeamento:
                coluna_destino = mapeamento[campo_origem]
                campos_mapeados[coluna_destino] = valor
        
        # Debug: mostrar campos mapeados
        logger.info(f"Campos mapeados para SinistrosControle: {campos_mapeados}")
        return campos_mapeados
    
    def _validar_tipos(self, dados: Dict) -> Dict:
        """Valida e converte tipos de dados para evitar erros SQL"""
        dados_validados = {}
        
        for campo, valor in dados.items():
            try:
                if valor is None:
                    dados_validados[campo] = None
                elif campo in ['nota_fiscal', 'numero_sinistro', 'status_geral', 'status_sinistro', 
                              'status_pagamento', 'numero_nd', 'status_indenizacao', 'responsavel_avaria',
                              'responsavel_compra_salvados', 'setor_responsavel', 'responsavel_interno',
                              'status_juridico', 'status_seguradora', 'nome_seguradora', 'usuario_criacao',
                              'usuario_atualizacao']:
                    # Campos que devem ser string
                    dados_validados[campo] = str(valor) if valor is not None else None
                elif campo in ['valor_indenizacao', 'valor_sinistro', 'valor_salvados_vendido', 
                              'valor_venda_salvados', 'percentual_desconto_salvados', 'valor_liberado',
                              'custas_juridicas']:
                    # Campos que devem ser numéricos
                    if isinstance(valor, (int, float)):
                        dados_validados[campo] = float(valor)
                    elif isinstance(valor, str):
                        try:
                            dados_validados[campo] = float(valor.replace(',', '.'))
                        except ValueError:
                            logger.warning(f"Valor inválido para campo numérico {campo}: {valor}")
                            dados_validados[campo] = 0.0
                    else:
                        dados_validados[campo] = 0.0
                elif campo in ['indenizado', 'acionamento_juridico', 'juridico_acionado', 
                              'acionamento_seguradora', 'seguro_acionado']:
                    # Campos booleanos
                    if isinstance(valor, bool):
                        dados_validados[campo] = valor
                    elif isinstance(valor, str):
                        dados_validados[campo] = valor.lower() in ['true', '1', 'sim', 'yes', 's', 'y']
                    else:
                        dados_validados[campo] = bool(valor)
                else:
                    # Outros campos - manter como string ou texto
                    dados_validados[campo] = str(valor) if valor is not None else None
                    
            except Exception as e:
                logger.error(f"Erro ao validar campo {campo} com valor {valor}: {e}")
                dados_validados[campo] = None
        
        logger.info(f"Dados após validação: {dados_validados}")
        return dados_validados
    
    def _tem_dados_pagamento(self, dados: Dict) -> bool:
        """Verifica se há dados de pagamento nos dados recebidos"""
        # Verificar se tem programacao_pagamento (lista)
        programacao = dados.get('programacao_pagamento', [])
        if programacao and isinstance(programacao, list):
            # Verificar se pelo menos um item tem dados preenchidos
            for item in programacao:
                if (item.get('data') or item.get('valor') or item.get('doctoESL')):
                    return True
        
        # Verificar campos individuais (fallback)
        campos_pagamento = ['data_pagamento', 'valor_pagamento', 'documento_esl', 'ordem']
        return any(campo in dados for campo in campos_pagamento)
    
    def _salvar_programacao_pagamento(self, sinistro_id: int, dados: Dict):
        """Salva dados de programação de pagamento"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Primeiro, limpar programações existentes
            cursor.execute("DELETE FROM [dbo].[ProgramacaoPagamento] WHERE [sinistro_id] = ?", [sinistro_id])
            
            # Obter lista de programação de pagamento
            programacao = dados.get('programacao_pagamento', [])
            
            if programacao and isinstance(programacao, list):
                sql = """
                INSERT INTO [dbo].[ProgramacaoPagamento] 
                ([sinistro_id], [data_pagamento], [valor_pagamento], [documento_esl], [ordem], [data_criacao], [data_atualizacao])
                VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())
                """
                
                for i, item in enumerate(programacao):
                    # Só salvar se pelo menos um campo estiver preenchido
                    if (item.get('data') or item.get('valor') or item.get('doctoESL')):
                        # Converter e validar dados
                        data_pag = item.get('data', '')
                        valor_pag = 0.0
                        try:
                            if item.get('valor'):
                                valor_pag = float(str(item.get('valor')).replace(',', '.'))
                        except ValueError:
                            valor_pag = 0.0
                        
                        documento = item.get('doctoESL', '')
                        ordem = i + 1
                        
                        cursor.execute(sql, [
                            sinistro_id,
                            data_pag if data_pag else None,
                            valor_pag,
                            documento if documento else None,
                            ordem
                        ])
                        
                        logger.info(f"Salvo pagamento {ordem}: data={data_pag}, valor={valor_pag}, doc={documento}")
            
            # Fallback para campos individuais
            elif any(campo in dados for campo in ['data_pagamento', 'valor_pagamento', 'documento_esl']):
                sql = """
                INSERT INTO [dbo].[ProgramacaoPagamento] 
                ([sinistro_id], [data_pagamento], [valor_pagamento], [documento_esl], [ordem], [data_criacao], [data_atualizacao])
                VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())
                """
                
                cursor.execute(sql, [
                    sinistro_id,
                    dados.get('data_pagamento'),
                    dados.get('valor_pagamento'),
                    dados.get('documento_esl'),
                    dados.get('ordem', 1)
                ])
            
            conn.commit()
            conn.close()
            
            logger.info(f"Programação de pagamento salva para sinistro ID: {sinistro_id}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar programação de pagamento: {e}")
    
    def _atualizar_programacao_pagamento(self, sinistro_id: int, dados: Dict):
        """Atualiza dados de programação de pagamento"""
        try:
            # Para atualização, usar o mesmo método de salvamento que limpa e recria
            self._salvar_programacao_pagamento(sinistro_id, dados)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar programação de pagamento: {e}")
    
    def listar_todos(self, limit: int = 1000000) -> List[Dict]:
        """Lista todos os sinistros da tabela SinistrosControle"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = f"""
            SELECT TOP {limit} s.*, p.data_pagamento, p.valor_pagamento, p.documento_esl, p.ordem
            FROM [dbo].[SinistrosControle] s
            LEFT JOIN [dbo].[ProgramacaoPagamento] p ON s.id = p.sinistro_id
            ORDER BY s.id DESC
            """
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