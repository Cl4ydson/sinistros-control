import React, { useState } from 'react';
import { ChevronDown, Check, Clock, AlertCircle, CheckCircle } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';

const StatusDropdown = ({ 
  currentStatus, 
  statusType = 'pagamento', 
  onStatusChange, 
  sinistroId,
  disabled = false 
}) => {
  const { isDark } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const statusOptions = {
    pagamento: {
      'Aguardando ND': { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: Clock },
      'Aguardando Pagamento': { color: 'bg-orange-100 text-orange-800 border-orange-200', icon: Clock },
      'Pago': { color: 'bg-green-100 text-green-800 border-green-200', icon: CheckCircle },
      'Em tratativa': { color: 'bg-blue-100 text-blue-800 border-blue-200', icon: AlertCircle }
    },
    indenizacao: {
      'Programado': { color: 'bg-blue-100 text-blue-800 border-blue-200', icon: Clock },
      'Pago': { color: 'bg-green-100 text-green-800 border-green-200', icon: CheckCircle },
      'Pendente': { color: 'bg-red-100 text-red-800 border-red-200', icon: AlertCircle },
      'Pago Parcial': { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: Clock }
    },
    juridico: {
      'Aguardando abertura': { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: Clock },
      'Processo iniciado': { color: 'bg-blue-100 text-blue-800 border-blue-200', icon: AlertCircle },
      'Indenizado': { color: 'bg-green-100 text-green-800 border-green-200', icon: CheckCircle }
    },
    seguradora: {
      'Aguardando abertura': { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: Clock },
      'Processo iniciado': { color: 'bg-blue-100 text-blue-800 border-blue-200', icon: AlertCircle },
      'Indenizado': { color: 'bg-green-100 text-green-800 border-green-200', icon: CheckCircle }
    }
  };

  const options = statusOptions[statusType] || statusOptions.pagamento;
  const currentStatusInfo = options[currentStatus] || { 
    color: 'bg-gray-100 text-gray-800 border-gray-200', 
    icon: AlertCircle 
  };
  const IconComponent = currentStatusInfo.icon;

  const handleStatusSelect = async (newStatus) => {
    if (newStatus === currentStatus || disabled) return;

    setIsUpdating(true);
    try {
      await onStatusChange(sinistroId, statusType, newStatus);
      setIsOpen(false);
    } catch (error) {
      console.error('Erro ao atualizar status:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  if (disabled) {
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${currentStatusInfo.color}`}>
        <IconComponent className="w-3 h-3 mr-1" />
        {currentStatus || 'N/A'}
      </span>
    );
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={isUpdating}
        className={`
          inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border
          ${currentStatusInfo.color}
          ${isUpdating ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-md transition-all cursor-pointer'}
          focus:outline-none focus:ring-2 focus:ring-blue-500/20
        `}
      >
        <IconComponent className={`w-3 h-3 mr-1 ${isUpdating ? 'animate-spin' : ''}`} />
        <span className="mr-1">{currentStatus || 'Selecionar'}</span>
        <ChevronDown className={`w-3 h-3 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <>
          {/* Overlay */}
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown */}
          <div className={`
            absolute right-0 mt-1 w-48 rounded-md shadow-lg z-20 border
            ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
          `}>
            <div className="py-1">
              {Object.entries(options).map(([status, statusInfo]) => {
                const StatusIcon = statusInfo.icon;
                const isSelected = status === currentStatus;
                
                return (
                  <button
                    key={status}
                    onClick={() => handleStatusSelect(status)}
                    className={`
                      w-full px-4 py-2 text-sm text-left flex items-center justify-between transition-colors
                      ${isDark 
                        ? 'text-gray-300 hover:bg-gray-700 hover:text-white' 
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }
                      ${isSelected ? (isDark ? 'bg-gray-700' : 'bg-gray-50') : ''}
                    `}
                  >
                    <div className="flex items-center">
                      <StatusIcon className="w-3 h-3 mr-2" />
                      <span>{status}</span>
                    </div>
                    {isSelected && <Check className="w-3 h-3 text-blue-500" />}
                  </button>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default StatusDropdown;