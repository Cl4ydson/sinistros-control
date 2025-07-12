import React from 'react';
import { AlertTriangle, CheckCircle, Info, X } from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';

const AlertCard = ({ 
  type = 'info', // info, warning, success, error
  title, 
  description, 
  onClose,
  actions = []
}) => {
  const { isDark } = useTheme();

  const alertTypes = {
    info: {
      icon: Info,
      bgColor: isDark ? 'bg-blue-900/50' : 'bg-blue-50',
      borderColor: 'border-blue-500',
      iconColor: 'text-blue-500',
      titleColor: isDark ? 'text-blue-300' : 'text-blue-800',
      textColor: isDark ? 'text-blue-200' : 'text-blue-700'
    },
    warning: {
      icon: AlertTriangle,
      bgColor: isDark ? 'bg-yellow-900/50' : 'bg-yellow-50',
      borderColor: 'border-yellow-500',
      iconColor: 'text-yellow-500',
      titleColor: isDark ? 'text-yellow-300' : 'text-yellow-800',
      textColor: isDark ? 'text-yellow-200' : 'text-yellow-700'
    },
    success: {
      icon: CheckCircle,
      bgColor: isDark ? 'bg-green-900/50' : 'bg-green-50',
      borderColor: 'border-green-500',
      iconColor: 'text-green-500',
      titleColor: isDark ? 'text-green-300' : 'text-green-800',
      textColor: isDark ? 'text-green-200' : 'text-green-700'
    },
    error: {
      icon: AlertTriangle,
      bgColor: isDark ? 'bg-red-900/50' : 'bg-red-50',
      borderColor: 'border-red-500',
      iconColor: 'text-red-500',
      titleColor: isDark ? 'text-red-300' : 'text-red-800',
      textColor: isDark ? 'text-red-200' : 'text-red-700'
    }
  };

  const currentAlert = alertTypes[type];
  const Icon = currentAlert.icon;

  return (
    <div className={`
      p-4 rounded-lg border-l-4 ${currentAlert.bgColor} ${currentAlert.borderColor}
      ${isDark ? 'border-gray-700' : 'border-gray-200'} border border-l-4
    `}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <Icon className={`w-5 h-5 mt-0.5 ${currentAlert.iconColor}`} />
          <div className="flex-1">
            <h4 className={`font-medium ${currentAlert.titleColor}`}>
              {title}
            </h4>
            {description && (
              <p className={`text-sm mt-1 ${currentAlert.textColor}`}>
                {description}
              </p>
            )}
            {actions.length > 0 && (
              <div className="mt-3 flex space-x-2">
                {actions.map((action, index) => (
                  <button
                    key={index}
                    onClick={action.onClick}
                    className={`
                      px-3 py-1 text-sm font-medium rounded-md transition-colors
                      ${action.variant === 'primary' 
                        ? `${currentAlert.iconColor.replace('text-', 'bg-')} text-white hover:opacity-90`
                        : `${currentAlert.textColor} hover:${currentAlert.bgColor}`
                      }
                    `}
                  >
                    {action.label}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
        
        {onClose && (
          <button
            onClick={onClose}
            className={`
              p-1 rounded-md transition-colors
              ${currentAlert.textColor} hover:${currentAlert.bgColor}
            `}
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};

export default AlertCard; 