from typing import List, Dict, Optional, Tuple
from datetime import datetime, date
import logging
from decimal import Decimal

from sqlalchemy.orm import Session
from ..database import get_db
from ..repositories.sinistro_automacao_repository import SinistroAutomacaoRepository
from ..repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
from ..schemas.sinistro_automacao import (
    SinistroAutomacaoCreate,
    SinistroAutomacaoUpdate,
    SinistroAutomacaoOut,
    SinistroAutomacaoResumo,
    EstatisticasSinistros
)
from ..models.sinistro_automacao import SinistroAutomacao

logger = logging.getLogger(__name__)

class SinistroAutomacaoService:
    """
    Service para gerenciar sinistros na tabela AUTOMACAO_BRSAMOR
    Inclui sincronização automática com banco origem e UPSERT
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.repo = SinistroAutomacaoRepository(db)
        self.repo_origem = SinistroRepositoryPyODBC()  # Para buscar dados do banco origem
    
    def sincronizar_sinistro_do_banco_origem(
        self, 
        nota_fiscal: str, 
        nr_conhecimento: Optional[str], 
        usuario: str
    ) -> Tuple[SinistroAutomacaoOut, bool]:
        """
        Sincroniza um sinistro específico do banco origem para AUTOMACAO_BRSAMOR
        Retorna: (sinistro, foi_criado)
        """
        try:
            # Buscar dados no banco origem
            dados_origem = self.repo_origem.buscar_sinistro_por_id(nota_fiscal, nr_conhecimento or "")
            
            if not dados_origem:
                raise ValueError(f"Sinistro não encontrado no banco origem: {nota_fiscal}/{nr_conhecimento}")
            
            # Converter dados do banco origem para schema de criação
            dados_criacao = self._converter_dados_origem(dados_origem)
            
            # Fazer UPSERT
            sinistro, foi_criado = self.repo.criar_ou_atualizar(dados_criacao, usuario)
            
            logger.info(f"Sinistro {'criado' if foi_criado else 'atualizado'}: {nota_fiscal}")
            
            return SinistroAutomacaoOut.from_orm(sinistro), foi_criado
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar sinistro: {e}")
            raise
    
    def _converter_dados_origem(self, dados_origem: Dict) -> SinistroAutomacaoCreate:
        """Converte dados do banco origem para schema de criação"""
        
        return SinistroAutomacaoCreate(
            nota_fiscal=dados_origem.get('Nota Fiscal', ''),
            nr_conhecimento=dados_origem.get('Minu.Conh'),
            remetente=dados_origem.get('Remetente'),
            destinatario=dados_origem.get('Destinatário'),
            cliente=dados_origem.get('Cliente'),  # Pode não existir na origem
            modal=dados_origem.get('Modal', 'Rodoviário'),
            
            # Datas
            dt_coleta=self._converter_data(dados_origem.get('Data Coleta')),
            dt_prazo_entrega=self._converter_data(dados_origem.get('Prazo Entrega')),
            dt_entrega_real=self._converter_data(dados_origem.get('Data Entrega')),
            dt_agendamento=self._converter_data(dados_origem.get('Data Agendamento')),
            dt_ocorrencia=self._converter_data(dados_origem.get('Data Ocorrência')),
            dt_cadastro=self._converter_data(dados_origem.get('Data Cadastro')),
            hr_cadastro=str(dados_origem.get('Hora Cadastro', ''))[:8] if dados_origem.get('Hora Cadastro') else None,
            dt_alteracao=self._converter_data(dados_origem.get('Data Alteração')),
            hr_alteracao=str(dados_origem.get('Hora Alteração', ''))[:8] if dados_origem.get('Hora Alteração') else None,
            
            # Ocorrências
            tipo_ocorrencia=dados_origem.get('Ocorrência'),
            descricao_ocorrencia=dados_origem.get('Compl. Ocorrência'),
            ultima_ocorrencia=dados_origem.get('ULTIMA OCORRENCIA'),
            referencia=dados_origem.get('REFERENCIA'),
            
            # Valor
            valor_mercadoria=self._converter_decimal(dados_origem.get('Valor Mercadoria', 0))
        )
    
    def _converter_data(self, data_valor) -> Optional[date]:
        """Converte valores de data para objeto date"""
        if not data_valor:
            return None
        
        if isinstance(data_valor, date):
            return data_valor
        
        if isinstance(data_valor, datetime):
            return data_valor.date()
        
        # Tentar converter string
        try:
            if isinstance(data_valor, str):
                return datetime.strptime(data_valor, '%Y-%m-%d').date()
        except:
            pass
        
        return None
    
    def _converter_decimal(self, valor) -> Decimal:
        """Converte valores para Decimal"""
        if valor is None:
            return Decimal('0')
        
        try:
            return Decimal(str(valor))
        except:
            return Decimal('0')
    
    def sincronizar_multiplos_sinistros(
        self, 
        filtros: Dict, 
        usuario: str,
        limite: int = 100
    ) -> Dict:
        """
        Sincroniza múltiplos sinistros do banco origem
        """
        try:
            # Buscar sinistros no banco origem
            sinistros_origem = self.repo_origem.listar_sinistros(**filtros)
            
            if not sinistros_origem:
                return {
                    'total_processados': 0,
                    'criados': 0,
                    'atualizados': 0,
                    'erros': 0,
                    'detalhes': []
                }
            
            # Limitar processamento
            sinistros_para_processar = sinistros_origem[:limite]
            
            criados = 0
            atualizados = 0
            erros = 0
            detalhes = []
            
            for dados_origem in sinistros_para_processar:
                try:
                    nota_fiscal = dados_origem.get('Nota Fiscal', '')
                    nr_conhecimento = dados_origem.get('Minu.Conh')
                    
                    # Sincronizar cada sinistro
                    sinistro, foi_criado = self.sincronizar_sinistro_do_banco_origem(
                        nota_fiscal, nr_conhecimento, usuario
                    )
                    
                    if foi_criado:
                        criados += 1
                    else:
                        atualizados += 1
                    
                    detalhes.append({
                        'nota_fiscal': nota_fiscal,
                        'nr_conhecimento': nr_conhecimento,
                        'acao': 'criado' if foi_criado else 'atualizado',
                        'sucesso': True
                    })
                    
                except Exception as e:
                    erros += 1
                    detalhes.append({
                        'nota_fiscal': dados_origem.get('Nota Fiscal', 'N/A'),
                        'nr_conhecimento': dados_origem.get('Minu.Conh', 'N/A'),
                        'acao': 'erro',
                        'sucesso': False,
                        'erro': str(e)
                    })
                    logger.error(f"Erro ao processar sinistro {dados_origem.get('Nota Fiscal')}: {e}")
            
            return {
                'total_processados': len(sinistros_para_processar),
                'criados': criados,
                'atualizados': atualizados,
                'erros': erros,
                'detalhes': detalhes
            }
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar múltiplos sinistros: {e}")
            raise
    
    def atualizar_sinistro(
        self, 
        sinistro_id: int, 
        dados: SinistroAutomacaoUpdate, 
        usuario: str
    ) -> Optional[SinistroAutomacaoOut]:
        """Atualiza campos específicos de um sinistro"""
        
        sinistro = self.repo.atualizar_campos_especificos(sinistro_id, dados, usuario)
        
        if sinistro:
            return SinistroAutomacaoOut.from_orm(sinistro)
        
        return None
    
    def buscar_sinistro(self, sinistro_id: int) -> Optional[SinistroAutomacaoOut]:
        """Busca sinistro por ID"""
        
        sinistro = self.repo.buscar_por_id(sinistro_id)
        
        if sinistro:
            return SinistroAutomacaoOut.from_orm(sinistro)
        
        return None
    
    def buscar_por_nota_conhecimento(
        self, 
        nota_fiscal: str, 
        nr_conhecimento: Optional[str] = None
    ) -> Optional[SinistroAutomacaoOut]:
        """Busca sinistro por nota e conhecimento"""
        
        sinistro = self.repo.buscar_por_nota_conhecimento(nota_fiscal, nr_conhecimento)
        
        if sinistro:
            return SinistroAutomacaoOut.from_orm(sinistro)
        
        return None
    
    def listar_sinistros(
        self,
        skip: int = 0,
        limit: int = 100,
        filtros: Optional[Dict] = None
    ) -> Tuple[List[SinistroAutomacaoResumo], int]:
        """Lista sinistros com paginação"""
        
        sinistros = self.repo.listar_sinistros(skip, limit, filtros)
        total = self.repo.contar_sinistros(filtros)
        
        sinistros_resumo = [
            SinistroAutomacaoResumo.from_orm(s) for s in sinistros
        ]
        
        return sinistros_resumo, total
    
    def obter_estatisticas(self) -> EstatisticasSinistros:
        """Obtém estatísticas dos sinistros"""
        
        stats = self.repo.obter_estatisticas()
        
        return EstatisticasSinistros(
            total_sinistros=stats.get('total_sinistros', 0),
            nao_iniciados=stats.get('nao_iniciados', 0),
            em_andamento=stats.get('em_andamento', 0),
            concluidos=stats.get('concluidos', 0),
            valor_total_sinistros=Decimal(str(stats.get('valor_total_sinistros', 0))),
            valor_total_prejuizo=Decimal(str(stats.get('valor_total_sinistros', 0))),  # Calcular prejuízo
            valor_total_indenizacoes=Decimal(str(stats.get('valor_total_indenizacoes', 0))),
            sinistros_com_acionamento_juridico=stats.get('sinistros_juridicos', 0),
            sinistros_com_acionamento_seguradora=stats.get('sinistros_seguradoras', 0)
        )
    
    def criar_sinistro_manual(
        self, 
        dados: SinistroAutomacaoCreate, 
        usuario: str
    ) -> SinistroAutomacaoOut:
        """Cria sinistro manualmente (sem sincronização)"""
        
        sinistro, _ = self.repo.criar_ou_atualizar(dados, usuario)
        
        return SinistroAutomacaoOut.from_orm(sinistro)
    
    def deletar_sinistro(self, sinistro_id: int) -> bool:
        """Deleta sinistro"""
        
        return self.repo.deletar(sinistro_id)

# Função de conveniência para criar service
def get_sinistro_automacao_service(db: Session = None) -> SinistroAutomacaoService:
    """Factory para criar SinistroAutomacaoService"""
    if db is None:
        db = next(get_db())
    
    return SinistroAutomacaoService(db) 