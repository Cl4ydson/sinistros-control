import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';

const StatsCard = ({ 
  title, 
  value, 
  icon: Icon, 
  trend, 
  trendValue, 
  color = 'blue',
  loading = false 
}) => {
  const { isDark } = useTheme();

  const colorClasses = {
    blue: {
      icon: 'bg-blue-500',
      trend: 'text-blue-600',
      accent: 'border-l-blue-500'
    },
    green: {
      icon: 'bg-green-500',
      trend: 'text-green-600',
      accent: 'border-l-green-500'
    },
    red: {
      icon: 'bg-red-500',
      trend: 'text-red-600',
      accent: 'border-l-red-500'
    },
    purple: {
      icon: 'bg-purple-500',
      trend: 'text-purple-600',
      accent: 'border-l-purple-500'
    },
    orange: {
      icon: 'bg-orange-500',
      trend: 'text-orange-600',
      accent: 'border-l-orange-500'
    }
  };

  const currentColor = colorClasses[color] || colorClasses.blue;

  if (loading) {
    return (
      <div className={`
        p-6 rounded-lg border border-l-4 ${currentColor.accent}
        ${isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}
        animate-pulse
      `}>
        <div className="flex items-center justify-between">
          <div className="space-y-3">
            <div className={`h-4 w-24 rounded ${isDark ? 'bg-gray-700' : 'bg-gray-200'}`} />
            <div className={`h-8 w-32 rounded ${isDark ? 'bg-gray-700' : 'bg-gray-200'}`} />
          </div>
          <div className={`w-12 h-12 rounded-lg ${isDark ? 'bg-gray-700' : 'bg-gray-200'}`} />
        </div>
      </div>
    );
  }

  return (
    <div className={`
      p-6 rounded-lg border border-l-4 ${currentColor.accent} transition-all duration-200 hover:shadow-lg
      ${isDark ? 'bg-gray-800 border-gray-700 hover:bg-gray-750' : 'bg-white border-gray-200 hover:shadow-xl'}
    `}>
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <p className={`text-sm font-medium ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>
            {title}
          </p>
          <p className={`text-3xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
            {value}
          </p>
          
          {trend && trendValue && (
            <div className="flex items-center space-x-2">
              {trend === 'up' ? (
                <TrendingUp className="w-4 h-4 text-green-500" />
              ) : (
                <TrendingDown className="w-4 h-4 text-red-500" />
              )}
              <span className={`text-sm font-medium ${
                trend === 'up' ? 'text-green-500' : 'text-red-500'
              }`}>
                {trendValue}
              </span>
              <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                vs. mês anterior
              </span>
            </div>
          )}
        </div>
        
        <div className={`w-12 h-12 ${currentColor.icon} rounded-lg flex items-center justify-center`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );
};

export default StatsCard; 