import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';

const ActionButton = ({ 
  title, 
  icon: Icon, 
  onClick,
  color = 'blue',
  variant = 'primary' // primary, secondary, outline
}) => {
  const { isDark } = useTheme();

  const colorClasses = {
    blue: {
      primary: `bg-blue-500 hover:bg-blue-600 text-white`,
      secondary: isDark 
        ? 'bg-blue-500/20 hover:bg-blue-500/30 text-blue-400' 
        : 'bg-blue-50 hover:bg-blue-100 text-blue-600',
      outline: isDark
        ? 'border-blue-500 text-blue-400 hover:bg-blue-500/20'
        : 'border-blue-300 text-blue-600 hover:bg-blue-50'
    },
    green: {
      primary: `bg-green-500 hover:bg-green-600 text-white`,
      secondary: isDark 
        ? 'bg-green-500/20 hover:bg-green-500/30 text-green-400' 
        : 'bg-green-50 hover:bg-green-100 text-green-600',
      outline: isDark
        ? 'border-green-500 text-green-400 hover:bg-green-500/20'
        : 'border-green-300 text-green-600 hover:bg-green-50'
    },
    purple: {
      primary: `bg-purple-500 hover:bg-purple-600 text-white`,
      secondary: isDark 
        ? 'bg-purple-500/20 hover:bg-purple-500/30 text-purple-400' 
        : 'bg-purple-50 hover:bg-purple-100 text-purple-600',
      outline: isDark
        ? 'border-purple-500 text-purple-400 hover:bg-purple-500/20'
        : 'border-purple-300 text-purple-600 hover:bg-purple-50'
    },
    orange: {
      primary: `bg-orange-500 hover:bg-orange-600 text-white`,
      secondary: isDark 
        ? 'bg-orange-500/20 hover:bg-orange-500/30 text-orange-400' 
        : 'bg-orange-50 hover:bg-orange-100 text-orange-600',
      outline: isDark
        ? 'border-orange-500 text-orange-400 hover:bg-orange-500/20'
        : 'border-orange-300 text-orange-600 hover:bg-orange-50'
    }
  };

  const currentColor = colorClasses[color] || colorClasses.blue;
  const baseClasses = `
    w-full p-4 rounded-lg font-medium transition-all duration-200 
    flex items-center justify-between group cursor-pointer
    ${variant === 'outline' ? 'border-2' : ''}
  `;

  return (
    <button
      onClick={onClick}
      className={`${baseClasses} ${currentColor[variant]}`}
    >
      <div className="flex items-center space-x-3">
        <Icon className="w-5 h-5" />
        <span>{title}</span>
      </div>
      <ArrowUpRight className="w-4 h-4 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
    </button>
  );
};

export default ActionButton; 