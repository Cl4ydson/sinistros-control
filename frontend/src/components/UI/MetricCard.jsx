import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';

const MetricCard = ({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  trend, 
  trendValue, 
  color = 'blue',
  onClick,
  className = ''
}) => {
  const { isDark } = useTheme();

  const colorClasses = {
    blue: {
      bg: isDark ? 'bg-slate-800/40 border-slate-700/50' : 'bg-blue-50 border-blue-200',
      icon: isDark ? 'text-blue-400' : 'text-blue-600',
      text: isDark ? 'text-blue-300' : 'text-blue-900',
      iconBg: isDark ? 'bg-slate-700/50 border-slate-600/50' : 'bg-blue-100 border-blue-200'
    },
    green: {
      bg: isDark ? 'bg-slate-800/40 border-slate-700/50' : 'bg-emerald-50 border-emerald-200',
      icon: isDark ? 'text-emerald-400' : 'text-emerald-600',
      text: isDark ? 'text-emerald-300' : 'text-emerald-900',
      iconBg: isDark ? 'bg-slate-700/50 border-slate-600/50' : 'bg-emerald-100 border-emerald-200'
    },
    red: {
      bg: isDark ? 'bg-slate-800/40 border-slate-700/50' : 'bg-red-50 border-red-200',
      icon: isDark ? 'text-red-400' : 'text-red-600',
      text: isDark ? 'text-red-300' : 'text-red-900',
      iconBg: isDark ? 'bg-slate-700/50 border-slate-600/50' : 'bg-red-100 border-red-200'
    },
    orange: {
      bg: isDark ? 'bg-slate-800/40 border-slate-700/50' : 'bg-orange-50 border-orange-200',
      icon: isDark ? 'text-orange-400' : 'text-orange-600',
      text: isDark ? 'text-orange-300' : 'text-orange-900',
      iconBg: isDark ? 'bg-slate-700/50 border-slate-600/50' : 'bg-orange-100 border-orange-200'
    },
    purple: {
      bg: isDark ? 'bg-slate-800/40 border-slate-700/50' : 'bg-purple-50 border-purple-200',
      icon: isDark ? 'text-purple-400' : 'text-purple-600',
      text: isDark ? 'text-purple-300' : 'text-purple-900',
      iconBg: isDark ? 'bg-slate-700/50 border-slate-600/50' : 'bg-purple-100 border-purple-200'
    }
  };

  const colors = colorClasses[color] || colorClasses.blue;

  const getTrendIcon = () => {
    if (trend === 'up') return '↗';
    if (trend === 'down') return '↘';
    return '→';
  };

  const getTrendColor = () => {
    if (trend === 'up') return 'text-green-500';
    if (trend === 'down') return 'text-red-500';
    return isDark ? 'text-slate-400' : 'text-gray-500';
  };

  return (
    <div 
      className={`
        p-6 rounded-2xl border transition-all duration-300 backdrop-blur-sm
        ${colors.bg}
        ${onClick ? 'cursor-pointer hover:scale-105 hover:shadow-lg' : ''}
        ${isDark ? 'hover:bg-opacity-80' : 'hover:bg-opacity-80'}
        ${className}
      `}
      onClick={onClick}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            {Icon && (
              <div className={`p-2 rounded-lg border ${colors.iconBg}`}>
                <Icon className={`w-5 h-5 ${colors.icon}`} />
              </div>
            )}
            <h3 className={`text-sm font-medium ${isDark ? 'text-white' : 'text-gray-600'}`}>
              {title}
            </h3>
          </div>
          
          <div className="mb-2">
            <p className={`text-2xl font-bold ${isDark ? 'text-white' : colors.text}`}>
              {value}
            </p>
            {subtitle && (
              <p className={`text-sm ${isDark ? 'text-slate-300' : 'text-gray-500'}`}>
                {subtitle}
              </p>
            )}
          </div>

          {(trend || trendValue) && (
            <div className="flex items-center space-x-1">
              {trend && (
                <span className={`text-sm font-medium ${getTrendColor()}`}>
                  {getTrendIcon()}
                </span>
              )}
              {trendValue && (
                <span className={`text-sm font-medium ${getTrendColor()}`}>
                  {trendValue}
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MetricCard; 