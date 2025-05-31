"""
Repositório de leitura dos sinistros diretamente no banco dtbTrans.

OBS.:
• Toda a lógica de SELECT fica encapsulada aqui: a service apenas orquestra.
• Não há mais definição de models ou de `SinistroResponse` neste arquivo
  – elas já existem em `backend/app/models/sinistro.py`.
"""

from typing import List, Dict, Optional
from datetime import date
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


class SinistroRepository:
    """Responsável por buscar sinistros, estatísticas e metadados."""

    def __init__(self, db):
        self.db = db

    # ------------------------------------------------------------------ #
    # Query base (sem filtros dinâmicos)
    # ------------------------------------------------------------------ #
    def _query_base(self) -> str:
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
                 ORDER  BY OCON2.id_OcorrenciaNota DESC
               )
        WHERE  OCO.ds_Ocorrencia IN (
                 'AVARIA PARCIAL','AVARIA TOTAL',
                 'EXTRAVIO TOTAL','EXTRAVIO PARCIAL',
                 'ROUBO DE CARGA','MERCADORIA SINISTRADA'
               )
        """

    # ------------------------------------------------------------------ #
    # Sinistros
    # ------------------------------------------------------------------ #
    def buscar_sinistros(
        self,
        dt_ini: Optional[date],
        dt_fim: Optional[date],
        cliente: Optional[str],
        nota_fiscal: Optional[str],
        conhecimento: Optional[str],
        limit: Optional[int] = None,          # None → sem limite
    ) -> List[Dict]:
        sql = self._query_base()
        params = {}

        # --- filtros dinâmicos ----------------------------------------- #
        if dt_ini:
            sql += " AND MOV.dt_Coleta >= :dt_ini"
            params["dt_ini"] = dt_ini
        if dt_fim:
            sql += " AND MOV.dt_Coleta <= :dt_fim"
            params["dt_fim"] = dt_fim
        if cliente:
            sql += " AND TRIM(MOV.ds_Cliente) LIKE :cliente"
            params["cliente"] = f"%{cliente}%"
        if nota_fiscal:
            sql += " AND OCN.nr_NotaFiscal = :nota_fiscal"
            params["nota_fiscal"] = nota_fiscal
        if conhecimento:
            sql += """
            AND (MOV.nr_Conhecimento = :conhecimento OR MOV.nr_Minuta = :conhecimento)
            """
            params["conhecimento"] = conhecimento

        sql += " ORDER BY OCN.dt_Abertura DESC"
        if limit:
            sql += " OFFSET 0 ROWS FETCH NEXT :limit ROWS ONLY"
            params["limit"] = limit

        logger.debug("SQL buscar_sinistros => %s | %s", sql, params)
        return self.db.execute(text(sql), params).mappings().all()

    def buscar_sinistro_por_id(
        self,
        nota_fiscal: str,
        conhecimento: str
    ) -> Optional[Dict]:
        sql = (
            self._query_base()
            + """
              AND OCN.nr_NotaFiscal = :nf
              AND (MOV.nr_Conhecimento = :conh OR MOV.nr_Minuta = :conh)
              """
        )
        row = self.db.execute(
            text(sql),
            {"nf": nota_fiscal, "conh": conhecimento}
        ).mappings().first()

        return row

    # ------------------------------------------------------------------ #
    # Estatísticas
    # ------------------------------------------------------------------ #
    def obter_estatisticas(
        self,
        dt_ini: Optional[date],
        dt_fim: Optional[date]
    ) -> Dict:
        sql = """
        SELECT
          COUNT(*)                                                     AS total_sinistros,
          SUM(CASE WHEN OCO.ds_Ocorrencia LIKE 'AVARIA%'  THEN 1 ELSE 0 END) AS avarias,
          SUM(CASE WHEN OCO.ds_Ocorrencia LIKE 'EXTRAVIO%'  THEN 1 ELSE 0 END) AS extravios,
          SUM(CASE WHEN OCO.ds_Ocorrencia LIKE 'ROUBO%' THEN 1 ELSE 0 END) AS roubos,
          SUM(CASE WHEN OCO.ds_Ocorrencia LIKE 'MERCADORIA SINISTRADA%' THEN 1 ELSE 0 END) AS sinistradas
        FROM tbdOcorrenciaNota OCN WITH (NOLOCK)
        INNER JOIN tbdOcorrencia      OCO WITH (NOLOCK) ON OCO.id_Ocorrencia = OCN.id_Ocorrencia
        INNER JOIN tbdMovimento       MOV WITH (NOLOCK) ON MOV.id_Movimento  = OCN.id_Movimento
        WHERE OCO.ds_Ocorrencia IN (
                 'AVARIA PARCIAL','AVARIA TOTAL',
                 'EXTRAVIO TOTAL','EXTRAVIO PARCIAL',
                 'ROUBO DE CARGA','MERCADORIA SINISTRADA'
               )
        """
        params = {}
        if dt_ini:
            sql += " AND MOV.dt_Coleta >= :dt_ini"
            params["dt_ini"] = dt_ini
        if dt_fim:
            sql += " AND MOV.dt_Coleta <= :dt_fim"
            params["dt_fim"] = dt_fim

        row = self.db.execute(text(sql), params).mappings().first()
        return (
            row
            if row
            else {"total_sinistros": 0, "avarias": 0, "extravios": 0, "roubos": 0, "sinistradas": 0}
        )

    # ------------------------------------------------------------------ #
    # Metadados
    # ------------------------------------------------------------------ #
    def obter_tipos_ocorrencia(self) -> List[str]:
        res = self.db.execute(
            text("SELECT DISTINCT ds_Ocorrencia FROM tbdOcorrencia ORDER BY ds_Ocorrencia")
        )
        return [r[0] for r in res]
