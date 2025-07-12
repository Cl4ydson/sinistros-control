import React from 'react';
import { Bell, Search, Menu } from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';
import ThemeToggle from '../ThemeToggle';

const Header = ({ title, subtitle, onToggleSidebar, showSearch = true }) => {
  const { isDark } = useTheme();

  return (
    <header className={`
      ${isDark ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200'} 
      border-b px-6 py-4 flex items-center justify-between
    `}>
      {/* Left Section */}
      <div className="flex items-center space-x-4">
        <button
          onClick={onToggleSidebar}
          className={`
            p-2 rounded-lg transition-colors lg:hidden
            ${isDark 
              ? 'hover:bg-gray-800 text-gray-400 hover:text-white' 
              : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
            }
          `}
        >
          <Menu className="w-5 h-5" />
        </button>
        
        <div>
          <h1 className={`text-2xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
            {title}
          </h1>
          {subtitle && (
            <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              {subtitle}
            </p>
          )}
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center space-x-4">
        {/* Search */}
        {showSearch && (
          <div className="relative hidden md:block">
            <Search className={`
              absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4
              ${isDark ? 'text-gray-400' : 'text-gray-500'}
            `} />
            <input
              type="text"
              placeholder="Buscar..."
              className={`
                pl-10 pr-4 py-2 rounded-lg border transition-colors w-64
                ${isDark 
                  ? 'bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:border-blue-500' 
                  : 'bg-gray-50 border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500'
                }
                focus:outline-none focus:ring-2 focus:ring-blue-500/20
              `}
            />
          </div>
        )}

        {/* Notifications */}
        <button className={`
          relative p-2 rounded-lg transition-colors
          ${isDark 
            ? 'hover:bg-gray-800 text-gray-400 hover:text-white' 
            : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
          }
        `}>
          <Bell className="w-5 h-5" />
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full flex items-center justify-center">
            <span className="text-white text-xs font-bold">3</span>
          </span>
        </button>

        {/* Theme Toggle */}
        <ThemeToggle />

        {/* User Avatar */}
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-medium">U</span>
          </div>
          <div className="hidden md:block">
            <p className={`text-sm font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
              Usuário Sistema
            </p>
            <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
              Administrador
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 