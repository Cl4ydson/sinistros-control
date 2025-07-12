import React, { useState, useEffect } from 'react';
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
  CheckCircle
} from 'lucide-react';
import MainLayout from '../components/Layout/MainLayout';
import { useTheme } from '../contexts/ThemeContext';

const SinistrosModern = () => {
  const { isDark } = useTheme();
  const [sinistros, setSinistros] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    status: '',
    dataInicio: '',
    dataFim: '',
    modal: ''
  });
  const [showFilters, setShowFilters] = useState(false);

  // Mock data para demonstração
  const mockSinistros = [
    {
      id: 1,
      numero: 'SIN-2024-001',
      cliente: 'Empresa ABC Ltda',
      dataOcorrencia: '2024-01-15',
      tipoOcorrencia: 'Avaria',
      status: 'Em Análise',
      valorPrejuizo: 15000.00,
      modal: 'Rodoviário',
      responsavel: 'João Silva'
    },
    {
      id: 2,
      numero: 'SIN-2024-002',
      cliente: 'Indústria XYZ SA',
      dataOcorrencia: '2024-01-18',
      tipoOcorrencia: 'Furto',
      status: 'Pendente',
      valorPrejuizo: 25000.00,
      modal: 'Aéreo',
      responsavel: 'Maria Santos'
    },
    {
      id: 3,
      numero: 'SIN-2024-003',
      cliente: 'Comércio 123 ME',
      dataOcorrencia: '2024-01-20',
      tipoOcorrencia: 'Atraso',
      status: 'Concluído',
      valorPrejuizo: 5000.00,
      modal: 'Rodoviário',
      responsavel: 'Pedro Costa'
    }
  ];

  useEffect(() => {
    loadSinistros();
  }, []);

  const loadSinistros = async () => {
    setLoading(true);
    try {
      // Simular API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSinistros(mockSinistros);
    } catch (error) {
      console.error('Erro ao carregar sinistros:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'concluído':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'em análise':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'pendente':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'aguardando':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status) => {
    switch (status.toLowerCase()) {
      case 'concluído':
        return <CheckCircle className="w-4 h-4" />;
      case 'em análise':
        return <Clock className="w-4 h-4" />;
      case 'pendente':
        return <AlertCircle className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const filteredSinistros = sinistros.filter(sinistro => {
    const matchesSearch = sinistro.numero.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         sinistro.cliente.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = !filters.status || sinistro.status === filters.status;
    const matchesModal = !filters.modal || sinistro.modal === filters.modal;
    
    return matchesSearch && matchesStatus && matchesModal;
  });

  return (
    <MainLayout 
      title="Sinistros" 
      subtitle="Gestão completa de sinistros"
      showSearch={false}
    >
      <div className="space-y-6">
        {/* Header Actions */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center space-x-4">
            {/* Search */}
            <div className="relative">
              <Search className={`
                absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4
                ${isDark ? 'text-gray-400' : 'text-gray-500'}
              `} />
              <input
                type="text"
                placeholder="Buscar sinistros..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className={`
                  pl-10 pr-4 py-2 rounded-lg border transition-colors w-64
                  ${isDark 
                    ? 'bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:border-blue-500' 
                    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500'
                  }
                  focus:outline-none focus:ring-2 focus:ring-blue-500/20
                `}
              />
            </div>

            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`
                p-2 rounded-lg border transition-colors
                ${isDark 
                  ? 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white hover:bg-gray-700' 
                  : 'bg-white border-gray-300 text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }
              `}
            >
              <Filter className="w-4 h-4" />
            </button>

            {/* Refresh */}
            <button
              onClick={loadSinistros}
              disabled={loading}
              className={`
                p-2 rounded-lg border transition-colors
                ${isDark 
                  ? 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white hover:bg-gray-700' 
                  : 'bg-white border-gray-300 text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }
                disabled:opacity-50 disabled:cursor-not-allowed
              `}
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>

          <div className="flex items-center space-x-3">
            <button className={`
              px-4 py-2 rounded-lg border transition-colors
              ${isDark 
                ? 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white hover:bg-gray-700' 
                : 'bg-white border-gray-300 text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }
            `}>
              <Download className="w-4 h-4 mr-2" />
              Exportar
            </button>
            
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              <Plus className="w-4 h-4 mr-2" />
              Novo Sinistro
            </button>
          </div>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className={`
            p-4 rounded-lg border
            ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
          `}>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  Status
                </label>
                <select
                  value={filters.status}
                  onChange={(e) => setFilters({...filters, status: e.target.value})}
                  className={`
                    w-full p-2 rounded-lg border
                    ${isDark 
                      ? 'bg-gray-700 border-gray-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                    }
                  `}
                >
                  <option value="">Todos</option>
                  <option value="Pendente">Pendente</option>
                  <option value="Em Análise">Em Análise</option>
                  <option value="Concluído">Concluído</option>
                </select>
              </div>

              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  Modal
                </label>
                <select
                  value={filters.modal}
                  onChange={(e) => setFilters({...filters, modal: e.target.value})}
                  className={`
                    w-full p-2 rounded-lg border
                    ${isDark 
                      ? 'bg-gray-700 border-gray-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                    }
                  `}
                >
                  <option value="">Todos</option>
                  <option value="Rodoviário">Rodoviário</option>
                  <option value="Aéreo">Aéreo</option>
                  <option value="Marítimo">Marítimo</option>
                </select>
              </div>

              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  Data Início
                </label>
                <input
                  type="date"
                  value={filters.dataInicio}
                  onChange={(e) => setFilters({...filters, dataInicio: e.target.value})}
                  className={`
                    w-full p-2 rounded-lg border
                    ${isDark 
                      ? 'bg-gray-700 border-gray-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                    }
                  `}
                />
              </div>

              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                  Data Fim
                </label>
                <input
                  type="date"
                  value={filters.dataFim}
                  onChange={(e) => setFilters({...filters, dataFim: e.target.value})}
                  className={`
                    w-full p-2 rounded-lg border
                    ${isDark 
                      ? 'bg-gray-700 border-gray-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                    }
                  `}
                />
              </div>
            </div>
          </div>
        )}

        {/* Sinistros Table */}
        <div className={`
          rounded-lg border overflow-hidden
          ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
        `}>
          {loading ? (
            <div className="p-8 text-center">
              <RefreshCw className={`w-8 h-8 animate-spin mx-auto mb-4 ${isDark ? 'text-gray-400' : 'text-gray-600'}`} />
              <p className={`${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                Carregando sinistros...
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className={`${isDark ? 'bg-gray-900' : 'bg-gray-50'}`}>
                  <tr>
                    <th className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${isDark ? 'text-gray-300' : 'text-gray-500'}`}>
                      Número
                    </th>
                    <th className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${isDark ? 'text-gray-300' : 'text-gray-500'}`}>
                      Cliente
                    </th>
                    <th className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${isDark ? 'text-gray-300' : 'text-gray-500'}`}>
                      Data
                    </th>
                    <th className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${isDark ? 'text-gray-300' : 'text-gray-500'}`}>
                      Tipo
                    </th>
                    <th className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${isDark ? 'text-gray-300' : 'text-gray-500'}`}>
                      Status
                    </th>
                    <th className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${isDark ? 'text-gray-300' : 'text-gray-500'}`}>
                      Valor
                    </th>
                    <th className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${isDark ? 'text-gray-300' : 'text-gray-500'}`}>
                      Ações
                    </th>
                  </tr>
                </thead>
                <tbody className={`divide-y ${isDark ? 'divide-gray-700' : 'divide-gray-200'}`}>
                  {filteredSinistros.map((sinistro) => (
                    <tr key={sinistro.id} className={`hover:${isDark ? 'bg-gray-700' : 'bg-gray-50'} transition-colors`}>
                      <td className={`px-6 py-4 whitespace-nowrap ${isDark ? 'text-white' : 'text-gray-900'}`}>
                        <div className="flex items-center">
                          <FileText className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="font-medium">{sinistro.numero}</span>
                        </div>
                      </td>
                      <td className={`px-6 py-4 whitespace-nowrap ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                        {sinistro.cliente}
                      </td>
                      <td className={`px-6 py-4 whitespace-nowrap ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                        {formatDate(sinistro.dataOcorrencia)}
                      </td>
                      <td className={`px-6 py-4 whitespace-nowrap ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                        {sinistro.tipoOcorrencia}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(sinistro.status)}`}>
                          {getStatusIcon(sinistro.status)}
                          <span className="ml-1">{sinistro.status}</span>
                        </span>
                      </td>
                      <td className={`px-6 py-4 whitespace-nowrap font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                        {formatCurrency(sinistro.valorPrejuizo)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button className={`p-1 rounded ${isDark ? 'text-gray-400 hover:text-blue-400' : 'text-gray-600 hover:text-blue-600'}`}>
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className={`p-1 rounded ${isDark ? 'text-gray-400 hover:text-green-400' : 'text-gray-600 hover:text-green-600'}`}>
                            <Edit className="w-4 h-4" />
                          </button>
                          <button className={`p-1 rounded ${isDark ? 'text-gray-400 hover:text-red-400' : 'text-gray-600 hover:text-red-600'}`}>
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Summary Stats */}
        <div className={`
          p-6 rounded-lg border
          ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
        `}>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <p className={`text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                {filteredSinistros.length}
              </p>
              <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                Total de Sinistros
              </p>
            </div>
            <div className="text-center">
              <p className={`text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                {formatCurrency(filteredSinistros.reduce((sum, s) => sum + s.valorPrejuizo, 0))}
              </p>
              <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                Valor Total em Prejuízos
              </p>
            </div>
            <div className="text-center">
              <p className={`text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                {filteredSinistros.filter(s => s.status === 'Concluído').length}
              </p>
              <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                Sinistros Concluídos
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default SinistrosModern; 