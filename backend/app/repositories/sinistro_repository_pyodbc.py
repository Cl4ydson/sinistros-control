"""
Repositório usando pyodbc diretamente para contornar problemas do SQLAlchemy
"""

import pyodbc
from typing import List, Dict, Optional
from datetime import date
import logging

logger = logging.getLogger(__name__)


class SinistroRepositoryPyODBC:
    """Repository usando pyodbc diretamente"""
    
    def __init__(self):
        self.conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=172.30.0.211;DATABASE=dtbTransporte;UID=consulta.pbi;PWD=naMf.}T3KVg+3fo6Z7Sq;TrustServerCertificate=yes;"
    
    def _get_connection(self):
        """Cria uma nova conexão"""
        return pyodbc.connect(self.conn_str)
    
    def _query_base(self) -> str:
        """Query base para sinistros - CORRIGIDA"""
        return """
        SELECT DISTINCT
               RTRIM(OCN.nr_NotaFiscal)      AS [Nota Fiscal],
               CASE WHEN UPPER(RTRIM(MOV.nr_Conhecimento)) = ''
                    THEN RTRIM(MOV.nr_Minuta)
                    ELSE UPPER(RTRIM(MOV.nr_Conhecimento))
               END                            AS [Minu.Conh],
               RTRIM(MOV.ds_Remetente)        AS [Remetente],
               TRIM(MOV.ds_Cliente)           AS [Destinatário],
               MOV.dt_Coleta                  AS [Data Coleta],
               RTRIM(OCO.ds_Ocorrencia)       AS [Ocorrência],
               RTRIM(OCN.ds_Ocorrencia)       AS [Compl. Ocorrência],
               TRIM(ULTOCO.ds_Ocorrencia)     AS [ULTIMA OCORRENCIA],
               MOV.nr_Referencia              AS [REFERENCIA],
               OCN.dt_PrazoFechamento         AS [Data Ocorrência],
               OCN.dt_Abertura                AS [Data Cadastro],
               OCN.hr_Abertura                AS [Hora Cadastro],
               OCN.dt_Alteracao               AS [Data Alteração],
               OCN.hr_Alteracao               AS [Hora Alteração]
        FROM   tbdOcorrenciaNota          OCN   WITH (NOLOCK)
        INNER  JOIN tbdOcorrencia         OCO   WITH (NOLOCK) ON OCN.id_Ocorrencia  = OCO.id_Ocorrencia
        INNER  JOIN tbdMovimento          MOV   WITH (NOLOCK) ON OCN.id_Movimento   = MOV.id_Movimento
        INNER  JOIN tbdMovimentoNotaFiscal MON  WITH (NOLOCK) ON OCN.id_Movimento   = MON.id_Movimento
        INNER  JOIN tbdMovimentoNotaFiscal MOVNF WITH (NOLOCK) ON MOV.id_Movimento   = MOVNF.id_Movimento
        LEFT   JOIN tbdOcorrencia         ULTOCO WITH (NOLOCK) ON ULTOCO.id_Ocorrencia = (
                 SELECT TOP 1 OCON2.id_Ocorrencia
                 FROM   tbdOcorrenciaNota OCON2 WITH (NOLOCK)
                 WHERE  OCON2.id_Movimento  = MOV.id_Movimento
                   AND  OCON2.nr_NotaFiscal = MOVNF.cd_NotaFiscal
                 ORDER BY OCON2.dt_Abertura DESC, OCON2.hr_Abertura DESC
               )
        WHERE  OCO.ds_Ocorrencia IN (
                 'AVARIA PARCIAL','AVARIA TOTAL',
                 'EXTRAVIO TOTAL','EXTRAVIO PARCIAL',
                 'ROUBO DE CARGA','MERCADORIA SINISTRADA'
               )
        """
    
    def buscar_sinistros(
        self,
        dt_ini: Optional[date] = None,
        dt_fim: Optional[date] = None,
        cliente: Optional[str] = None,
        nota_fiscal: Optional[str] = None,
        conhecimento: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """Busca sinistros com filtros - SEM ORDER BY problemático"""
        
        # Query super simples que FUNCIONA
        limit_clause = f"TOP {limit if limit else 10}"
        
        sql = f"""
        SELECT DISTINCT {limit_clause}
            OCN.nr_NotaFiscal AS [Nota Fiscal],
            OCO.ds_Ocorrencia AS [Ocorrência],
            MOV.ds_Cliente AS [Destinatário],
            MOV.ds_Remetente AS [Remetente],
            MOV.dt_Coleta AS [Data Coleta],
            OCN.ds_Ocorrencia AS [Compl. Ocorrência],
            '' AS [ULTIMA OCORRENCIA],
            MOV.nr_Referencia AS [REFERENCIA],
            OCN.dt_PrazoFechamento AS [Data Ocorrência],
            OCN.dt_Abertura AS [Data Cadastro],
            OCN.hr_Abertura AS [Hora Cadastro],
            OCN.dt_Alteracao AS [Data Alteração],
            OCN.hr_Alteracao AS [Hora Alteração],
            CASE WHEN UPPER(RTRIM(MOV.nr_Conhecimento)) = ''
                 THEN RTRIM(MOV.nr_Minuta)
                 ELSE UPPER(RTRIM(MOV.nr_Conhecimento))
            END AS [Minu.Conh]
        FROM tbdOcorrenciaNota OCN WITH (NOLOCK)
        INNER JOIN tbdOcorrencia OCO WITH (NOLOCK) ON OCN.id_Ocorrencia = OCO.id_Ocorrencia
        INNER JOIN tbdMovimento MOV WITH (NOLOCK) ON OCN.id_Movimento = MOV.id_Movimento
        WHERE OCO.ds_Ocorrencia IN (
            'AVARIA PARCIAL','AVARIA TOTAL',
            'EXTRAVIO TOTAL','EXTRAVIO PARCIAL', 
            'ROUBO DE CARGA','MERCADORIA SINISTRADA'
        )
        """
        
        params = []
        
        # Filtros opcionais
        if dt_ini:
            sql += " AND MOV.dt_Coleta >= ?"
            params.append(dt_ini)
        if dt_fim:
            sql += " AND MOV.dt_Coleta <= ?"
            params.append(dt_fim)
        if cliente:
            sql += " AND MOV.ds_Cliente LIKE ?"
            params.append(f"%{cliente}%")
        if nota_fiscal:
            sql += " AND OCN.nr_NotaFiscal = ?"
            params.append(nota_fiscal)
        if conhecimento:
            sql += " AND (MOV.nr_Conhecimento = ? OR MOV.nr_Minuta = ?)"
            params.extend([conhecimento, conhecimento])
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            
            # Converter para dicionários
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                row_dict = {columns[i]: (value.strip() if isinstance(value, str) else value) 
                           for i, value in enumerate(row)}
                results.append(row_dict)
            
            conn.close()
            print(f"✅ Encontrados {len(results)} sinistros")
            return results
            
        except Exception as e:
            print(f"❌ Erro ao buscar sinistros: {e}")
            logger.error(f"Erro detalhado ao buscar sinistros: {e}")
            raise
    
    def buscar_sinistro_por_id(
        self,
        nota_fiscal: str,
        conhecimento: str
    ) -> Optional[Dict]:
        """Busca um sinistro específico - CORRIGIDA"""
        
        sql = """
        SELECT DISTINCT TOP 1
               RTRIM(OCN.nr_NotaFiscal)      AS [Nota Fiscal],
               CASE WHEN UPPER(RTRIM(MOV.nr_Conhecimento)) = ''
                    THEN RTRIM(MOV.nr_Minuta)
                    ELSE UPPER(RTRIM(MOV.nr_Conhecimento))
               END                            AS [Minu.Conh],
               RTRIM(MOV.ds_Remetente)        AS [Remetente],
               TRIM(MOV.ds_Cliente)           AS [Destinatário],
               MOV.dt_Coleta                  AS [Data Coleta],
               RTRIM(OCO.ds_Ocorrencia)       AS [Ocorrência],
               RTRIM(OCN.ds_Ocorrencia)       AS [Compl. Ocorrência],
               COALESCE(ULTOCO.ds_Ocorrencia, '') AS [ULTIMA OCORRENCIA],
               MOV.nr_Referencia              AS [REFERENCIA],
               OCN.dt_PrazoFechamento         AS [Data Ocorrência],
               OCN.dt_Abertura                AS [Data Cadastro],
               OCN.hr_Abertura                AS [Hora Cadastro],
               OCN.dt_Alteracao               AS [Data Alteração],
               OCN.hr_Alteracao               AS [Hora Alteração]
        FROM   tbdOcorrenciaNota          OCN   WITH (NOLOCK)
        INNER  JOIN tbdOcorrencia         OCO   WITH (NOLOCK) ON OCN.id_Ocorrencia  = OCO.id_Ocorrencia
        INNER  JOIN tbdMovimento          MOV   WITH (NOLOCK) ON OCN.id_Movimento   = MOV.id_Movimento
        LEFT   JOIN tbdOcorrencia         ULTOCO WITH (NOLOCK) ON ULTOCO.id_Ocorrencia = (
                 SELECT TOP 1 OCN2.id_Ocorrencia
                 FROM   tbdOcorrenciaNota OCN2 WITH (NOLOCK)
                 WHERE  OCN2.id_Movimento = MOV.id_Movimento
                 ORDER BY OCN2.dt_Abertura DESC, OCN2.hr_Abertura DESC
               )
        WHERE  OCO.ds_Ocorrencia IN (
                 'AVARIA PARCIAL','AVARIA TOTAL',
                 'EXTRAVIO TOTAL','EXTRAVIO PARCIAL',
                 'ROUBO DE CARGA','MERCADORIA SINISTRADA'
               )
        AND OCN.nr_NotaFiscal = ?
        AND (MOV.nr_Conhecimento = ? OR MOV.nr_Minuta = ?)
        ORDER BY OCN.dt_Abertura DESC
        """
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, [nota_fiscal, conhecimento, conhecimento])
            
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            
            if row:
                result = {}
                for i, value in enumerate(row):
                    result[columns[i]] = value.strip() if isinstance(value, str) else value
                conn.close()
                return result
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar sinistro por ID: {e}")
            raise
    
    def obter_estatisticas(
        self,
        dt_ini: Optional[date] = None,
        dt_fim: Optional[date] = None
    ) -> Dict:
        """Obtém estatísticas dos sinistros"""
        
        sql = """
        SELECT
          COUNT(*) AS total_sinistros,
          SUM(CASE WHEN OCO.ds_Ocorrencia LIKE 'AVARIA%' THEN 1 ELSE 0 END) AS avarias,
          SUM(CASE WHEN OCO.ds_Ocorrencia LIKE 'EXTRAVIO%' THEN 1 ELSE 0 END) AS extravios,
          SUM(CASE WHEN OCO.ds_Ocorrencia LIKE 'ROUBO%' THEN 1 ELSE 0 END) AS roubos,
          SUM(CASE WHEN OCO.ds_Ocorrencia LIKE 'MERCADORIA SINISTRADA%' THEN 1 ELSE 0 END) AS sinistradas
        FROM tbdOcorrenciaNota OCN WITH (NOLOCK)
        INNER JOIN tbdOcorrencia OCO WITH (NOLOCK) ON OCO.id_Ocorrencia = OCN.id_Ocorrencia
        INNER JOIN tbdMovimento MOV WITH (NOLOCK) ON MOV.id_Movimento = OCN.id_Movimento
        WHERE OCO.ds_Ocorrencia IN (
                 'AVARIA PARCIAL','AVARIA TOTAL',
                 'EXTRAVIO TOTAL','EXTRAVIO PARCIAL',
                 'ROUBO DE CARGA','MERCADORIA SINISTRADA'
               )
        """
        
        params = []
        if dt_ini:
            sql += " AND MOV.dt_Coleta >= ?"
            params.append(dt_ini)
        if dt_fim:
            sql += " AND MOV.dt_Coleta <= ?"
            params.append(dt_fim)
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'total_sinistros': row[0] or 0,
                    'avarias': row[1] or 0,
                    'extravios': row[2] or 0,
                    'roubos': row[3] or 0,
                    'sinistradas': row[4] or 0
                }
            else:
                return {'total_sinistros': 0, 'avarias': 0, 'extravios': 0, 'roubos': 0, 'sinistradas': 0}
                
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            raise
    
    def obter_tipos_ocorrencia(self) -> List[str]:
        """Obtém lista de tipos de ocorrência"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT ds_Ocorrencia FROM tbdOcorrencia ORDER BY ds_Ocorrencia")
            
            results = [row[0] for row in cursor.fetchall()]
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Erro ao obter tipos de ocorrência: {e}")
            raise 

    def test_connection(self) -> bool:
        """Testa a conexão com o banco"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            conn.close()
            print("✅ Conexão com banco de dados OK")
            return True
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False