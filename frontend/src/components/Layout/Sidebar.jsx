import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  Users, 
  Settings, 
  BarChart3,
  History,
  AlertTriangle,
  LogOut,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';

const Sidebar = ({ isCollapsed, toggleSidebar }) => {
  const location = useLocation();
  const { isDark } = useTheme();

  const menuItems = [
    {
      icon: LayoutDashboard,
      label: 'Dashboard',
      path: '/dashboard',
      color: 'text-blue-500'
    },
    {
      icon: FileText,
      label: 'Sinistros',
      path: '/sinistros',
      color: 'text-green-500'
    },
    {
      icon: BarChart3,
      label: 'Relatórios',
      path: '/relatorios',
      color: 'text-purple-500'
    },
    {
      icon: History,
      label: 'Histórico',
      path: '/historico',
      color: 'text-orange-500'
    },
    {
      icon: AlertTriangle,
      label: 'Alertas',
      path: '/alertas',
      color: 'text-red-500'
    },
    {
      icon: Users,
      label: 'Usuários',
      path: '/usuarios',
      color: 'text-cyan-500'
    },
    {
      icon: Settings,
      label: 'Configurações',
      path: '/configuracoes',
      color: 'text-gray-500'
    }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div className={`
      ${isCollapsed ? 'w-16' : 'w-64'} 
      ${isDark ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200'} 
      border-r transition-all duration-300 h-screen fixed left-0 top-0 z-50 flex flex-col
    `}>
      {/* Header */}
      <div className={`
        ${isDark ? 'border-gray-700' : 'border-gray-200'} 
        border-b p-4 flex items-center justify-between
      `}>
        {!isCollapsed && (
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className={`font-bold text-lg ${isDark ? 'text-white' : 'text-gray-900'}`}>
                BR SAMOR
              </h1>
              <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                Sistema BRSAMOR
              </p>
            </div>
          </div>
        )}
        
        <button
          onClick={toggleSidebar}
          className={`
            p-2 rounded-lg transition-colors
            ${isDark 
              ? 'hover:bg-gray-800 text-gray-400 hover:text-white' 
              : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
            }
          `}
        >
          {isCollapsed ? (
            <ChevronRight className="w-4 h-4" />
          ) : (
            <ChevronLeft className="w-4 h-4" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);
            
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`
                    flex items-center p-3 rounded-lg transition-all duration-200 group
                    ${active
                      ? `${isDark ? 'bg-blue-600' : 'bg-blue-50'} ${isDark ? 'text-white' : 'text-blue-700'}`
                      : `${isDark ? 'text-gray-300 hover:bg-gray-800 hover:text-white' : 'text-gray-700 hover:bg-gray-100'}`
                    }
                  `}
                  title={isCollapsed ? item.label : ''}
                >
                  <Icon className={`
                    w-5 h-5 
                    ${active ? 'text-current' : item.color}
                    ${isCollapsed ? '' : 'mr-3'}
                  `} />
                  {!isCollapsed && (
                    <span className="font-medium">{item.label}</span>
                  )}
                  {active && !isCollapsed && (
                    <div className="ml-auto w-2 h-2 bg-current rounded-full opacity-60" />
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* User Section */}
      <div className={`
        ${isDark ? 'border-gray-700' : 'border-gray-200'} 
        border-t p-4
      `}>
        <div className={`
          flex items-center p-3 rounded-lg transition-colors
          ${isDark ? 'hover:bg-gray-800' : 'hover:bg-gray-100'}
        `}>
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-medium">U</span>
          </div>
          {!isCollapsed && (
            <div className="ml-3 flex-1">
              <p className={`text-sm font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Usuário Logado
              </p>
              <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                Sistema BRSAMOR
              </p>
            </div>
          )}
        </div>
        
        {!isCollapsed && (
          <button className={`
            w-full mt-3 flex items-center justify-center p-2 rounded-lg transition-colors
            ${isDark 
              ? 'text-gray-400 hover:bg-gray-800 hover:text-red-400' 
              : 'text-gray-600 hover:bg-red-50 hover:text-red-600'
            }
          `}>
            <LogOut className="w-4 h-4 mr-2" />
            Sair
          </button>
        )}
      </div>
    </div>
  );
};

export default Sidebar; 