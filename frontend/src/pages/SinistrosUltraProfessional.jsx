import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { 
  FileText, 
  Search, 
  Filter, 
  Plus, 
  Eye, 
  Edit, 
  Trash2,
  Download,
  RefreshCw,
  Calendar,
  DollarSign,
  Clock,
  AlertCircle,
  CheckCircle,
  TrendingUp,
  BarChart3,
  Users,
  MapPin,
  Truck,
  Shield,
  Zap,
  Star,
  ArrowUpRight,
  MoreVertical,
  Archive,
  Send,
  FileCheck,
  Database,
  Activity,
  Layers,
  Filter as FilterIcon,
  Save,
  X
} from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { useNavigate } from 'react-router-dom';
import SinistrosAPI from '../services/api';
import { LoadingSpinner, MetricCard, DataTable } from '../components';
import UltraProfessionalLayout from '../components/Layout/UltraProfessionalLayout';

// Componente Modal de Visualização usando Portal
const ModalVisualizacao = ({ sinistro, isDark, onClose, onEdit }) => {
  // Função para fechar com ESC
  React.useEffect(() => {
    const handleEscKey = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscKey);
    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [onClose]);

  // Função para formatar datas
  const formatDate = (dateString) => {
    if (!dateString) return '-';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR');
    } catch (error) {
      return dateString;
    }
  };

  // Função para formatar moeda
  const formatCurrency = (value) => {
    if (!value) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0
    }).format(value);
  };

  return (
    <div 
      className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-[9999] p-4"
      style={{ 
        position: 'fixed', 
        top: 0, 
        left: 0, 
        right: 0, 
        bottom: 0,
        margin: 0,
        zIndex: 9999 
      }}
      onClick={onClose}
    >
      <div 
        className={`
          max-w-6xl w-full max-h-[90vh] overflow-y-auto rounded-2xl border shadow-2xl
          ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'}
          relative z-[10000]
        `}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header do Modal */}
        <div className={`
          flex items-center justify-between p-6 border-b sticky top-0 z-10
          ${isDark ? 'border-slate-700 bg-slate-800' : 'border-gray-200 bg-white'}
        `}>
          <div>
            <h2 className={`text-2xl font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Detalhes do Sinistro
            </h2>
            <p className={`text-sm ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
              Conhecimento: {sinistro.nr_conhecimento}
            </p>
          </div>
          <button
            onClick={onClose}
            className={`
              p-2 rounded-lg transition-colors hover:scale-105
              ${isDark ? 'hover:bg-slate-700 text-slate-400' : 'hover:bg-gray-100 text-gray-600'}
            `}
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Conteúdo do Modal */}
        <div className="p-6 space-y-6">
          {/* Informações Básicas */}
          <div className={`
            p-6 rounded-2xl border
            ${isDark ? 'bg-slate-700/30 border-slate-600' : 'bg-gray-50/60 border-gray-200'}
          `}>
            <h3 className={`text-lg font-semibold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Informações Básicas
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <DetailField label="Nota Fiscal" value={sinistro.nota_fiscal} isDark={isDark} />
              <DetailField label="Conhecimento" value={sinistro.nr_conhecimento} isDark={isDark} />
              <DetailField label="Remetente" value={sinistro.remetente} isDark={isDark} />
              <DetailField label="Destinatário" value={sinistro.cliente} isDark={isDark} />
              <DetailField label="Modal" value={sinistro.modal} isDark={isDark} />
              <DetailField label="Referência" value={sinistro.referencia} isDark={isDark} />
            </div>
          </div>

          {/* Datas */}
          <div className={`
            p-6 rounded-2xl border
            ${isDark ? 'bg-slate-700/30 border-slate-600' : 'bg-gray-50/60 border-gray-200'}
          `}>
            <h3 className={`text-lg font-semibold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Cronologia
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <DetailField label="Data Coleta" value={formatDate(sinistro.data_coleta)} isDark={isDark} />
              <DetailField label="Prazo Entrega" value={formatDate(sinistro.prazo_entrega)} isDark={isDark} />
              <DetailField label="Data Entrega" value={formatDate(sinistro.data_entrega)} isDark={isDark} />
              <DetailField label="Data Evento" value={formatDate(sinistro.data_evento)} isDark={isDark} />
              <DetailField label="Data Agendamento" value={formatDate(sinistro.data_agendamento)} isDark={isDark} />
              <DetailField label="Data Cadastro" value={formatDate(sinistro.data_cadastro)} isDark={isDark} />
            </div>
          </div>

          {/* Ocorrência */}
          <div className={`
            p-6 rounded-2xl border
            ${isDark ? 'bg-slate-700/30 border-slate-600' : 'bg-gray-50/60 border-gray-200'}
          `}>
            <h3 className={`text-lg font-semibold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Detalhes da Ocorrência
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <DetailField label="Tipo de Ocorrência" value={sinistro.tipo_ocorrencia} isDark={isDark} />
              <DetailField label="Status" value={sinistro.status} isDark={isDark} />
              <DetailField 
                label="Descrição da Ocorrência" 
                value={sinistro.descricao_ocorrencia} 
                isDark={isDark} 
                isLarge={true}
              />
              <DetailField 
                label="Última Ocorrência" 
                value={sinistro.ultima_ocorrencia} 
                isDark={isDark} 
                isLarge={true}
              />
            </div>
          </div>

          {/* Valores */}
          <div className={`
            p-6 rounded-2xl border
            ${isDark ? 'bg-slate-700/30 border-slate-600' : 'bg-gray-50/60 border-gray-200'}
          `}>
            <h3 className={`text-lg font-semibold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Valores
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <DetailField 
                label="Valor da Mercadoria" 
                value={formatCurrency(sinistro.valor_mercadoria)} 
                isDark={isDark} 
              />
              <DetailField 
                label="Valor do Sinistro" 
                value={formatCurrency(sinistro.valor_sinistro || 0)} 
                isDark={isDark} 
              />
            </div>
          </div>

          {/* Tempos */}
          <div className={`
            p-6 rounded-2xl border
            ${isDark ? 'bg-slate-700/30 border-slate-600' : 'bg-gray-50/60 border-gray-200'}
          `}>
            <h3 className={`text-lg font-semibold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Horários
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <DetailField label="Hora Cadastro" value={sinistro.hora_cadastro} isDark={isDark} />
              <DetailField label="Hora Alteração" value={sinistro.hora_alteracao} isDark={isDark} />
              <DetailField label="Data Alteração" value={formatDate(sinistro.data_alteracao)} isDark={isDark} />
            </div>
          </div>
        </div>

        {/* Footer do Modal */}
        <div className={`
          flex items-center justify-between p-6 border-t sticky bottom-0
          ${isDark ? 'border-slate-700 bg-slate-800' : 'border-gray-200 bg-white'}
        `}>
          <button
            onClick={onEdit}
            className="flex items-center space-x-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all hover:scale-105 shadow-lg"
          >
            <Edit className="w-4 h-4" />
            <span>Editar Sinistro</span>
          </button>
          
          <button
            onClick={onClose}
            className={`
              px-6 py-3 rounded-lg border transition-all hover:scale-105 shadow-md
              ${isDark 
                ? 'border-slate-600 hover:bg-slate-700 text-slate-300' 
                : 'border-gray-300 hover:bg-gray-50 text-gray-700'
              }
            `}
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
};

const SinistrosUltraProfessional = () => {
  const { isDark } = useTheme();
  const navigate = useNavigate();
  
  // Estados
  const [sinistros, setSinistros] = useState([]);
  const [estatisticas, setEstatisticas] = useState({});
  const [loading, setLoading] = useState(false);
  const [loadingStats, setLoadingStats] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filtros, setFiltros] = useState({
    dt_ini: '',
    dt_fim: '',
    cliente: '',
    nota_fiscal: '',
    conhecimento: '',
    limit: 100 // Busca 100 registros iniciais
  });
  const [showFilters, setShowFilters] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState(null);

  // Estados para o modal de visualização
  const [showModal, setShowModal] = useState(false);
  const [selectedSinistro, setSelectedSinistro] = useState(null);

  const breadcrumbs = ['Sistema', 'Sinistros'];

  const headerActions = [
    { 
      icon: RefreshCw, 
      onClick: () => loadInitialData(),
      tooltip: 'Atualizar dados' 
    },
    { 
      icon: Download, 
      onClick: () => console.log('Export sinistros'),
      tooltip: 'Exportar dados' 
    },
    { 
      icon: FilterIcon, 
      onClick: () => setShowFilters(!showFilters),
      tooltip: 'Filtros avançados' 
    }
  ];

  // Colunas da tabela ULTRATHINK
  const columns = [
    {
      key: 'nota_fiscal',
      label: 'Nota Fiscal',
      sortable: true,
      className: 'font-mono text-sm'
    },
    {
      key: 'nr_conhecimento',
      label: 'Conhecimento',
      sortable: true,
      className: 'font-mono text-sm'
    },
    {
      key: 'remetente',
      label: 'Remetente',
      sortable: true,
      className: 'max-w-48 truncate'
    },
    {
      key: 'cliente',
      label: 'Destinatário',
      sortable: true,
      className: 'max-w-48 truncate'
    },
    {
      key: 'data_coleta',
      label: 'Data Coleta',
      type: 'date',
      sortable: true
    },
    {
      key: 'tipo_ocorrencia',
      label: 'Tipo Ocorrência',
      sortable: true,
      className: 'font-medium'
    },
    {
      key: 'status',
      label: 'Status',
      sortable: true
    },
    {
      key: 'referencia',
      label: 'Referência',
      sortable: true,
      className: 'font-mono text-sm'
    }
  ];

  // Carregar dados iniciais
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    await Promise.all([
      loadSinistros(),
      loadEstatisticas(),
      testConnection()
    ]);
  };

  const testConnection = async () => {
    try {
      const result = await SinistrosAPI.testarConexao();
      setConnectionStatus(result);
    } catch (error) {
      console.error('Erro ao testar conexão:', error);
      setConnectionStatus({ success: false, message: 'Erro na conexão' });
    }
  };

  const loadSinistros = async (customFilters = {}) => {
    setLoading(true);
    setError(null);
    try {
      const filterParams = { ...filtros, ...customFilters };
      const result = await SinistrosAPI.listarSinistros(filterParams);
      
      if (result.success) {
        setSinistros(result.data.items || []);
      } else {
        setError('Erro ao carregar sinistros');
      }
    } catch (error) {
      console.error('Erro ao carregar sinistros:', error);
      setError('Erro ao conectar com o servidor');
    } finally {
      setLoading(false);
    }
  };

  const loadEstatisticas = async () => {
    setLoadingStats(true);
    try {
      const result = await SinistrosAPI.obterEstatisticas();
      if (result.success) {
        setEstatisticas(result.data);
      }
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    } finally {
      setLoadingStats(false);
    }
  };

  const handleEditarSinistro = (sinistro) => {
    // Usar nota_fiscal + conhecimento como ID único
    const sinistroId = `${sinistro.nota_fiscal}-${sinistro.nr_conhecimento}`;
    navigate(`/sinistros/editar/${sinistroId}`);
  };

  const handleViewSinistro = (sinistro) => {
    setSelectedSinistro(sinistro);
    setShowModal(true);
  };

  const handleApplyFilters = () => {
    loadSinistros(filtros);
    setShowFilters(false);
  };

  const handleClearFilters = () => {
    const clearedFilters = {
      dt_ini: '',
      dt_fim: '',
      cliente: '',
      nota_fiscal: '',
      conhecimento: '',
      limit: 100
    };
    setFiltros(clearedFilters);
    loadSinistros(clearedFilters);
  };

  const formatCurrency = (value) => {
    if (!value) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0
    }).format(value);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR');
    } catch (error) {
      return dateString;
    }
  };

  const getMetricColor = (type) => {
    const colors = {
      total: 'blue',
      avarias: 'orange',
      extravios: 'red',
      roubos: 'purple',
      sinistradas: 'green'
    };
    return colors[type] || 'blue';
  };

  return (
    <UltraProfessionalLayout 
      title="Central de Sinistros" 
      subtitle="Gestão Ultra Profissional de Sinistros em Tempo Real • Dados reais do banco"
      breadcrumbs={breadcrumbs}
      headerActions={headerActions}
    >
      {/* Header com status */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          {/* Status da Conexão */}
          {connectionStatus && (
            <div className={`
              flex items-center space-x-2 px-4 py-2 rounded-lg border
              ${connectionStatus.success 
                ? (isDark ? 'bg-emerald-900/30 border-emerald-700 text-emerald-400' : 'bg-emerald-50 border-emerald-200 text-emerald-700')
                : (isDark ? 'bg-red-900/30 border-red-700 text-red-400' : 'bg-red-50 border-red-200 text-red-700')
              }
            `}>
              <Database className="w-4 h-4" />
              <span className="text-sm font-medium">
                {connectionStatus.success ? 'Conectado' : 'Desconectado'}
              </span>
            </div>
          )}

          <div className={`
            px-4 py-2 rounded-lg border text-sm font-medium
            ${isDark ? 'bg-blue-900/30 border-blue-700 text-blue-400' : 'bg-blue-50 border-blue-200 text-blue-700'}
          `}>
            📊 {estatisticas.total_sinistros || 0} sinistros encontrados
          </div>
        </div>
      </div>

      {/* Métricas ULTRATHINK */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
        {loadingStats ? (
          <div className="col-span-full">
            <LoadingSpinner size="small" message="Carregando estatísticas..." />
          </div>
        ) : (
          <>
            <MetricCard
              title="Total de Sinistros"
              value={estatisticas.total_sinistros || 0}
              icon={FileText}
              color={getMetricColor('total')}
              trend="up"
              trendValue="+12%"
            />
            <MetricCard
              title="Avarias"
              value={estatisticas.avarias || 0}
              icon={AlertCircle}
              color={getMetricColor('avarias')}
              trend="down"
              trendValue="-5%"
            />
            <MetricCard
              title="Extravios"
              value={estatisticas.extravios || 0}
              icon={Search}
              color={getMetricColor('extravios')}
              trend="up"
              trendValue="+3%"
            />
            <MetricCard
              title="Roubos"
              value={estatisticas.roubos || 0}
              icon={Shield}
              color={getMetricColor('roubos')}
              trend="down"
              trendValue="-8%"
            />
            <MetricCard
              title="Mercadorias Sinistradas"
              value={estatisticas.sinistradas || 0}
              icon={CheckCircle}
              color={getMetricColor('sinistradas')}
              trend="up"
              trendValue="+15%"
            />
          </>
        )}
      </div>

      {/* Filtros Avançados */}
      {showFilters && (
        <div className={`
          mb-6 p-6 rounded-2xl border backdrop-blur-sm
          ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
        `}>
          <h3 className="text-lg font-semibold mb-4">Filtros Avançados</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                Data Inicial
              </label>
              <input
                type="date"
                value={filtros.dt_ini}
                onChange={(e) => setFiltros({...filtros, dt_ini: e.target.value})}
                className={`
                  w-full px-4 py-2 rounded-lg border
                  ${isDark 
                    ? 'bg-slate-700 border-slate-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-900'
                  }
                `}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                Data Final
              </label>
              <input
                type="date"
                value={filtros.dt_fim}
                onChange={(e) => setFiltros({...filtros, dt_fim: e.target.value})}
                className={`
                  w-full px-4 py-2 rounded-lg border
                  ${isDark 
                    ? 'bg-slate-700 border-slate-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-900'
                  }
                `}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                Cliente
              </label>
              <input
                type="text"
                placeholder="Nome do cliente..."
                value={filtros.cliente}
                onChange={(e) => setFiltros({...filtros, cliente: e.target.value})}
                className={`
                  w-full px-4 py-2 rounded-lg border
                  ${isDark 
                    ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400' 
                    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
                  }
                `}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                Nota Fiscal
              </label>
              <input
                type="text"
                placeholder="Número da NF..."
                value={filtros.nota_fiscal}
                onChange={(e) => setFiltros({...filtros, nota_fiscal: e.target.value})}
                className={`
                  w-full px-4 py-2 rounded-lg border
                  ${isDark 
                    ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400' 
                    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
                  }
                `}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                Conhecimento
              </label>
              <input
                type="text"
                placeholder="Número do conhecimento..."
                value={filtros.conhecimento}
                onChange={(e) => setFiltros({...filtros, conhecimento: e.target.value})}
                className={`
                  w-full px-4 py-2 rounded-lg border
                  ${isDark 
                    ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400' 
                    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
                  }
                `}
              />
            </div>
            <div>
              <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                Limite de Registros
              </label>
              <select
                value={filtros.limit}
                onChange={(e) => setFiltros({...filtros, limit: Number(e.target.value)})}
                className={`
                  w-full px-4 py-2 rounded-lg border
                  ${isDark 
                    ? 'bg-slate-700 border-slate-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-900'
                  }
                `}
              >
                <option value={50}>50 registros</option>
                <option value={100}>100 registros</option>
                <option value={500}>500 registros</option>
                <option value={1000}>1.000 registros</option>
                <option value={0}>Todos os registros</option>
              </select>
            </div>
            
            <div className="col-span-full flex space-x-4 mt-4">
              <button
                onClick={handleApplyFilters}
                className="flex items-center space-x-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
              >
                <Search className="w-4 h-4" />
                <span>Aplicar Filtros</span>
              </button>
              <button
                onClick={handleClearFilters}
                className={`
                  flex items-center space-x-2 px-6 py-2 rounded-lg border transition-colors
                  ${isDark 
                    ? 'border-slate-600 hover:bg-slate-700 text-slate-300' 
                    : 'border-gray-300 hover:bg-gray-50 text-gray-700'
                  }
                `}
              >
                <RefreshCw className="w-4 h-4" />
                <span>Limpar Filtros</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Tabela de Dados ULTRATHINK */}
      {error ? (
        <div className={`
          p-8 text-center rounded-2xl border backdrop-blur-sm
          ${isDark ? 'bg-red-900/30 border-red-700 text-red-400' : 'bg-red-50 border-red-200 text-red-700'}
        `}>
          <AlertCircle className="w-12 h-12 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">Erro ao Carregar Dados</h3>
          <p className="mb-4">{error}</p>
          <button
            onClick={() => loadInitialData()}
            className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
          >
            Tentar Novamente
          </button>
        </div>
      ) : (
        <DataTable
          data={sinistros}
          columns={columns}
          loading={loading}
          onRowClick={handleViewSinistro}
          onEdit={handleEditarSinistro}
          onView={handleViewSinistro}
          pageSize={20}
          searchable={true}
          filterable={false} // Filtros já estão na seção dedicada
          exportable={true}
        />
      )}

      {/* Footer com informações */}
      <div className={`
        mt-8 p-4 rounded-2xl border text-center backdrop-blur-sm
        ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
      `}>
        <div className="flex items-center justify-center space-x-6 text-sm">
          <div className="flex items-center space-x-2">
            <Activity className={`w-4 h-4 ${isDark ? 'text-green-400' : 'text-green-600'}`} />
            <span className={isDark ? 'text-slate-300' : 'text-gray-700'}>
              Sistema Online
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <Database className={`w-4 h-4 ${isDark ? 'text-blue-400' : 'text-blue-600'}`} />
            <span className={isDark ? 'text-slate-300' : 'text-gray-700'}>
              Dados em Tempo Real
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <Layers className={`w-4 h-4 ${isDark ? 'text-purple-400' : 'text-purple-600'}`} />
            <span className={isDark ? 'text-slate-300' : 'text-gray-700'}>
              ULTRATHINK v2.0
            </span>
          </div>
        </div>
      </div>

      {/* Modal de Visualização renderizado via Portal */}
      {showModal && selectedSinistro && createPortal(
        <ModalVisualizacao 
          sinistro={selectedSinistro}
          isDark={isDark}
          onClose={() => setShowModal(false)}
          onEdit={() => {
            setShowModal(false);
            handleEditarSinistro(selectedSinistro);
          }}
        />,
        document.body
      )}
    </UltraProfessionalLayout>
  );
};

// Componente para exibir campos de detalhes no modal
const DetailField = ({ label, value, isDark = false, isLarge = false }) => (
  <div className={isLarge ? "md:col-span-2" : ""}>
    <label className={`block text-sm font-medium mb-1 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
      {label}
    </label>
    <div className={`
      p-3 rounded-lg border ${isLarge ? 'min-h-[60px]' : 'min-h-[44px]'}
      ${isDark ? 'bg-slate-800 border-slate-600 text-slate-200' : 'bg-gray-50 border-gray-200 text-gray-900'}
    `}>
      {value || '-'}
    </div>
  </div>
);

export default SinistrosUltraProfessional; 