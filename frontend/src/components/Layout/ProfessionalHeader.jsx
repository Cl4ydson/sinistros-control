import React, { useState } from 'react';
import { 
  Bell, 
  Search, 
  Menu, 
  Settings, 
  Calendar,
  Filter,
  Download,
  Plus,
  RefreshCw,
  MoreHorizontal,
  ChevronRight,
  Globe,
  Zap,
  Clock
} from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';
import ThemeToggle from '../ThemeToggle';

const ProfessionalHeader = ({ 
  title, 
  subtitle, 
  breadcrumbs = [],
  onToggleSidebar, 
  showSearch = true,
  actions = []
}) => {
  const { isDark } = useTheme();
  
  const [notifications] = useState([
    { id: 1, type: 'urgent', message: '5 sinistros precisam de atenção', time: '2 min' },
    { id: 2, type: 'info', message: 'Relatório mensal disponível', time: '15 min' },
    { id: 3, type: 'success', message: 'Backup realizado com sucesso', time: '1h' }
  ]);
  const [showNotifications, setShowNotifications] = useState(false);

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'urgent': return <Zap className="w-4 h-4 text-red-500" />;
      case 'info': return <Bell className="w-4 h-4 text-blue-500" />;
      case 'success': return <Globe className="w-4 h-4 text-green-500" />;
      default: return <Bell className="w-4 h-4" />;
    }
  };

  return (
    <header className={`
      ${isDark 
        ? 'bg-slate-900/95 border-slate-700 backdrop-blur-xl' 
        : 'bg-white/95 border-gray-200 backdrop-blur-xl'
      } 
      border-b px-6 py-4 sticky top-0 z-40
    `}>
      <div className="flex items-center justify-between">
        {/* Left Section */}
        <div className="flex items-center space-x-6">
          <button
            onClick={onToggleSidebar}
            className={`
              p-2.5 rounded-xl transition-all duration-200 lg:hidden
              ${isDark 
                ? 'hover:bg-slate-800 text-slate-400 hover:text-white' 
                : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
              }
            `}
          >
            <Menu className="w-5 h-5" />
          </button>
          
          <div className="flex flex-col">
            {/* Breadcrumbs */}
            {breadcrumbs.length > 0 && (
              <nav className="flex items-center space-x-2 mb-1">
                {breadcrumbs.map((crumb, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <span className={`
                      text-sm ${index === breadcrumbs.length - 1 
                        ? (isDark ? 'text-white font-medium' : 'text-gray-900 font-medium')
                        : (isDark ? 'text-slate-400 hover:text-white' : 'text-gray-500 hover:text-gray-900')
                      }
                      ${index < breadcrumbs.length - 1 ? 'cursor-pointer' : ''}
                    `}>
                      {crumb}
                    </span>
                    {index < breadcrumbs.length - 1 && (
                      <ChevronRight className={`w-3 h-3 ${isDark ? 'text-slate-600' : 'text-gray-400'}`} />
                    )}
                  </div>
                ))}
              </nav>
            )}
            
            {/* Title - ULTRATHINK FIX: Using React state directly for reliability */}
            <div className="flex items-center space-x-3">
              <h1 
                className={`text-2xl font-bold transition-colors duration-200 ultrathink-title`}
                style={{
                  color: isDark ? '#ffffff' : '#111827'
                }}
                data-theme={isDark ? 'dark' : 'light'}
              >
                {title}
              </h1>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-gray-500'}`}>
                  Online
                </span>
              </div>
            </div>
            
            {subtitle && (
              <p className={`text-sm mt-1 ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
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
                absolute left-4 top-1/2 transform -translate-y-1/2 w-4 h-4
                ${isDark ? 'text-slate-400' : 'text-gray-500'}
              `} />
              <input
                type="text"
                placeholder="Buscar em tudo..."
                className={`
                  pl-11 pr-4 py-3 rounded-xl border transition-all duration-200 w-80
                  ${isDark 
                    ? 'bg-slate-800/60 border-slate-700 text-white placeholder-slate-400 focus:border-blue-500 focus:bg-slate-800' 
                    : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:bg-white'
                  }
                  focus:outline-none focus:ring-2 focus:ring-blue-500/20 backdrop-blur-sm
                `}
              />
            </div>
          )}

          {/* Action Buttons */}
          {actions.length > 0 && (
            <div className="flex items-center space-x-2">
              {actions.map((action, index) => (
                <button
                  key={index}
                  onClick={action.onClick}
                  className={`
                    p-2.5 rounded-xl transition-all duration-200 group
                    ${action.variant === 'primary' 
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
                      : `${isDark 
                          ? 'hover:bg-slate-800 text-slate-400 hover:text-white' 
                          : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
                        }`
                    }
                  `}
                >
                  <action.icon className="w-5 h-5 group-hover:scale-110 transition-transform" />
                </button>
              ))}
            </div>
          )}

          {/* Quick Actions */}
          <div className="hidden lg:flex items-center space-x-2">
            <button className={`
              p-2.5 rounded-xl transition-colors
              ${isDark 
                ? 'hover:bg-slate-800 text-slate-400 hover:text-white' 
                : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
              }
            `}>
              <Filter className="w-4 h-4" />
            </button>
            <button className={`
              p-2.5 rounded-xl transition-colors
              ${isDark 
                ? 'hover:bg-slate-800 text-slate-400 hover:text-white' 
                : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
              }
            `}>
              <Download className="w-4 h-4" />
            </button>
            <button className={`
              p-2.5 rounded-xl transition-colors
              ${isDark 
                ? 'hover:bg-slate-800 text-slate-400 hover:text-white' 
                : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
              }
            `}>
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>

          {/* Notifications */}
          <div className="relative">
            <button 
              onClick={() => setShowNotifications(!showNotifications)}
              className={`
                relative p-2.5 rounded-xl transition-colors
                ${isDark 
                  ? 'hover:bg-slate-800 text-slate-400 hover:text-white' 
                  : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
                }
              `}
            >
              <Bell className="w-5 h-5" />
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-gradient-to-r from-red-500 to-pink-500 rounded-full flex items-center justify-center">
                <span className="text-white text-xs font-bold">{notifications.length}</span>
              </span>
            </button>

            {/* Notifications Dropdown */}
            {showNotifications && (
              <div className={`
                absolute right-0 top-full mt-2 w-80 rounded-xl shadow-2xl border z-50
                ${isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200'}
                backdrop-blur-xl
              `}>
                <div className={`p-4 border-b ${isDark ? 'border-slate-700' : 'border-gray-200'}`}>
                  <h3 className={`font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    Notificações
                  </h3>
                </div>
                <div className="max-h-64 overflow-y-auto">
                  {notifications.map((notification) => (
                    <div key={notification.id} className={`
                      p-4 border-b last:border-b-0 hover:bg-opacity-50 transition-colors
                      ${isDark ? 'border-slate-700 hover:bg-slate-700' : 'border-gray-100 hover:bg-gray-50'}
                    `}>
                      <div className="flex items-start space-x-3">
                        {getNotificationIcon(notification.type)}
                        <div className="flex-1">
                          <p className={`text-sm ${isDark ? 'text-white' : 'text-gray-900'}`}>
                            {notification.message}
                          </p>
                          <div className="flex items-center mt-1">
                            <Clock className={`w-3 h-3 mr-1 ${isDark ? 'text-slate-400' : 'text-gray-500'}`} />
                            <span className={`text-xs ${isDark ? 'text-slate-400' : 'text-gray-500'}`}>
                              {notification.time} atrás
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className={`p-3 text-center border-t ${isDark ? 'border-slate-700' : 'border-gray-200'}`}>
                  <button className={`text-sm font-medium ${isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'}`}>
                    Ver todas as notificações
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Theme Toggle */}
          <ThemeToggle />

          {/* Settings */}
          <button className={`
            p-2.5 rounded-xl transition-colors
            ${isDark 
              ? 'hover:bg-slate-800 text-slate-400 hover:text-white' 
              : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
            }
          `}>
            <Settings className="w-5 h-5" />
          </button>

          {/* User Profile */}
          <div className="flex items-center space-x-3 pl-4 border-l border-slate-700">
            <div className="hidden md:block text-right">
              <p className={`text-sm font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Sistema Admin
              </p>
              <p className={`text-xs ${isDark ? 'text-slate-400' : 'text-gray-500'}`}>
                Acesso Total
              </p>
            </div>
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-r from-violet-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
                <span className="text-white text-sm font-bold">SA</span>
              </div>
              <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default ProfessionalHeader; 