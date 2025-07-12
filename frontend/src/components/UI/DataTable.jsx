import React, { useState, useMemo } from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import { ChevronLeft, ChevronRight, Search, Filter, Download, Eye, Edit, MoreVertical } from 'lucide-react';

const DataTable = ({ 
  data = [], 
  columns = [], 
  loading = false,
  onRowClick,
  onEdit,
  onView,
  searchable = true,
  filterable = true,
  exportable = true,
  pageSize = 20,
  className = ''
}) => {
  const { isDark } = useTheme();
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  // Filtrar e pesquisar dados
  const filteredData = useMemo(() => {
    if (!searchTerm) return data;
    
    return data.filter(item =>
      Object.values(item).some(value =>
        value?.toString().toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [data, searchTerm]);

  // Ordenar dados
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData;

    return [...filteredData].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (aValue < bValue) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (aValue > bValue) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }, [filteredData, sortConfig]);

  // Paginar dados
  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * pageSize;
    return sortedData.slice(startIndex, startIndex + pageSize);
  }, [sortedData, currentPage, pageSize]);

  const totalPages = Math.ceil(sortedData.length / pageSize);

  const handleSort = (key) => {
    setSortConfig(prevConfig => ({
      key,
      direction: prevConfig.key === key && prevConfig.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const formatValue = (value, column) => {
    if (value === null || value === undefined) return '-';
    
    if (column.type === 'currency') {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value);
    }
    
    if (column.type === 'date') {
      return new Date(value).toLocaleDateString('pt-BR');
    }
    
    if (column.type === 'datetime') {
      return new Date(value).toLocaleString('pt-BR');
    }

    if (column.format) {
      return column.format(value);
    }
    
    return value.toString();
  };

  const getStatusColor = (status) => {
    const statusColors = {
      'concluído': 'bg-emerald-100 text-emerald-800 border-emerald-200',
      'em análise': 'bg-blue-100 text-blue-800 border-blue-200',
      'pendente': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'cancelado': 'bg-red-100 text-red-800 border-red-200'
    };
    
    return statusColors[status?.toLowerCase()] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
    );
  }

  return (
    <div className={`rounded-2xl border ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'} ${className}`}>
      {/* Header da Tabela */}
      {(searchable || filterable || exportable) && (
        <div className="p-6 border-b border-gray-200 dark:border-slate-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {searchable && (
                <div className="relative">
                  <Search className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 ${isDark ? 'text-slate-400' : 'text-gray-500'}`} />
                  <input
                    type="text"
                    placeholder="Pesquisar..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className={`
                      pl-10 pr-4 py-2 rounded-lg border
                      ${isDark 
                        ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400' 
                        : 'bg-gray-50 border-gray-300 text-gray-900 placeholder-gray-500'
                      }
                    `}
                  />
                </div>
              )}
              {filterable && (
                <button className={`
                  p-2 rounded-lg border transition-colors
                  ${isDark 
                    ? 'border-slate-600 hover:bg-slate-700 text-slate-400' 
                    : 'border-gray-300 hover:bg-gray-50 text-gray-600'
                  }
                `}>
                  <Filter className="w-4 h-4" />
                </button>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              <span className={`text-sm ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                {sortedData.length} registros
              </span>
              {exportable && (
                <button className={`
                  p-2 rounded-lg border transition-colors
                  ${isDark 
                    ? 'border-slate-600 hover:bg-slate-700 text-slate-400' 
                    : 'border-gray-300 hover:bg-gray-50 text-gray-600'
                  }
                `}>
                  <Download className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Tabela */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className={`${isDark ? 'bg-slate-700' : 'bg-gray-50'}`}>
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={`
                    px-6 py-4 text-left text-xs font-medium uppercase tracking-wider cursor-pointer
                    ${isDark ? 'text-slate-300' : 'text-gray-500'}
                    ${column.sortable !== false ? 'hover:bg-opacity-80' : ''}
                  `}
                  onClick={() => column.sortable !== false && handleSort(column.key)}
                >
                  <div className="flex items-center space-x-1">
                    <span>{column.label}</span>
                    {sortConfig.key === column.key && (
                      <span className="text-blue-500">
                        {sortConfig.direction === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </div>
                </th>
              ))}
              <th className={`px-6 py-4 text-right text-xs font-medium uppercase tracking-wider ${isDark ? 'text-slate-300' : 'text-gray-500'}`}>
                Ações
              </th>
            </tr>
          </thead>
          <tbody className={`divide-y ${isDark ? 'divide-slate-700' : 'divide-gray-200'}`}>
            {paginatedData.map((row, index) => (
              <tr 
                key={index}
                className={`
                  transition-colors
                  ${onRowClick ? 'cursor-pointer' : ''}
                  ${isDark ? 'hover:bg-slate-700' : 'hover:bg-gray-50'}
                `}
                onClick={() => onRowClick && onRowClick(row)}
              >
                {columns.map((column) => (
                  <td key={column.key} className={`px-6 py-4 whitespace-nowrap ${isDark ? 'text-slate-300' : 'text-gray-900'}`}>
                    {column.key === 'status' ? (
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(row[column.key])}`}>
                        {formatValue(row[column.key], column)}
                      </span>
                    ) : (
                      <div className={column.className || ''}>
                        {formatValue(row[column.key], column)}
                      </div>
                    )}
                  </td>
                ))}
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex items-center justify-end space-x-2">
                    {onView && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onView(row);
                        }}
                        className={`p-1 rounded hover:bg-gray-100 dark:hover:bg-slate-600 ${isDark ? 'text-slate-400' : 'text-gray-600'}`}
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    )}
                    {onEdit && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onEdit(row);
                        }}
                        className={`p-1 rounded hover:bg-gray-100 dark:hover:bg-slate-600 ${isDark ? 'text-slate-400' : 'text-gray-600'}`}
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                    )}
                    <button className={`p-1 rounded hover:bg-gray-100 dark:hover:bg-slate-600 ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Paginação */}
      {totalPages > 1 && (
        <div className="px-6 py-4 border-t border-gray-200 dark:border-slate-700">
          <div className="flex items-center justify-between">
            <div className={`text-sm ${isDark ? 'text-slate-400' : 'text-gray-700'}`}>
              Mostrando {((currentPage - 1) * pageSize) + 1} até {Math.min(currentPage * pageSize, sortedData.length)} de {sortedData.length} registros
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className={`
                  p-2 rounded-lg border transition-colors
                  ${currentPage === 1 ? 'opacity-50 cursor-not-allowed' : ''}
                  ${isDark 
                    ? 'border-slate-600 hover:bg-slate-700 text-slate-400' 
                    : 'border-gray-300 hover:bg-gray-50 text-gray-600'
                  }
                `}
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              
              <span className={`px-4 py-2 text-sm font-medium ${isDark ? 'text-slate-300' : 'text-gray-900'}`}>
                {currentPage} de {totalPages}
              </span>
              
              <button
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className={`
                  p-2 rounded-lg border transition-colors
                  ${currentPage === totalPages ? 'opacity-50 cursor-not-allowed' : ''}
                  ${isDark 
                    ? 'border-slate-600 hover:bg-slate-700 text-slate-400' 
                    : 'border-gray-300 hover:bg-gray-50 text-gray-600'
                  }
                `}
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataTable; 