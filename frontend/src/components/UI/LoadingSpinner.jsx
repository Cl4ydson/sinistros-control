import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';

const LoadingSpinner = ({ size = 'medium', message = 'Carregando...' }) => {
  const { isDark } = useTheme();
  
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-12 h-12',
    large: 'w-16 h-16'
  };

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className={`
        animate-spin rounded-full border-4 border-solid
        ${isDark ? 'border-slate-600' : 'border-gray-300'}
        ${isDark ? 'border-t-blue-400' : 'border-t-blue-600'}
        ${sizeClasses[size]}
      `} />
      {message && (
        <p className={`mt-4 text-sm font-medium ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
          {message}
        </p>
      )}
    </div>
  );
};

export default LoadingSpinner; 