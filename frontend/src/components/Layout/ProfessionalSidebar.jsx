import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  BarChart3,
  AlertTriangle,
  Settings,
  Users,
  Calendar,
  TrendingUp,
  Shield,
  Database,
  Bell,
  Search,
  Plus,
  Filter,
  Download,
  ChevronLeft,
  ChevronRight,
  User,
  LogOut,
  Home
} from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';

const ProfessionalSidebar = ({ isCollapsed, toggleSidebar }) => {
  const location = useLocation();
  const { isDark } = useTheme();

  const menuSections = [
    {
      title: 'Principal',
      items: [
        {
          icon: Home,
          label: 'Início',
          path: '/dashboard',
          color: 'text-blue-500',
          gradient: 'from-blue-500 to-blue-600'
        },
        {
          icon: FileText,
          label: 'Sinistros',
          path: '/sinistros',
          color: 'text-emerald-500',
          gradient: 'from-emerald-500 to-emerald-600',
          badge: '42'
        }
      ]
    },
    {
      title: 'Análise',
      items: [
        {
          icon: BarChart3,
          label: 'Relatórios',
          path: '/relatorios',
          color: 'text-purple-500',
          gradient: 'from-purple-500 to-purple-600'
        },
        {
          icon: TrendingUp,
          label: 'Analytics',
          path: '/analytics',
          color: 'text-orange-500',
          gradient: 'from-orange-500 to-orange-600'
        },
        {
          icon: Calendar,
          label: 'Histórico',
          path: '/historico',
          color: 'text-cyan-500',
          gradient: 'from-cyan-500 to-cyan-600'
        }
      ]
    },
    {
      title: 'Gestão',
      items: [
        {
          icon: AlertTriangle,
          label: 'Alertas',
          path: '/alertas',
          color: 'text-red-500',
          gradient: 'from-red-500 to-red-600',
          badge: '5'
        },
        {
          icon: Users,
          label: 'Usuários',
          path: '/usuarios',
          color: 'text-indigo-500',
          gradient: 'from-indigo-500 to-indigo-600'
        },
        {
          icon: Database,
          label: 'Sistema',
          path: '/sistema',
          color: 'text-gray-500',
          gradient: 'from-gray-500 to-gray-600'
        }
      ]
    }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <div className={`
      ${isCollapsed ? 'w-20' : 'w-72'} 
      transition-all duration-300 h-screen fixed left-0 top-0 z-50 flex flex-col
      ${isDark 
        ? 'bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 border-slate-700' 
        : 'bg-gradient-to-b from-white via-gray-50 to-white border-gray-300'
      } 
      border-r backdrop-blur-xl
    `}>
      {/* Header */}
      <div className={`
        ${isDark ? 'border-slate-700' : 'border-gray-200'} 
        border-b p-6 flex items-center justify-between
        ${isDark ? 'bg-slate-900/80' : 'bg-white/80'} backdrop-blur-sm
      `}>
        {!isCollapsed && (
          <div className="flex items-center space-x-4">
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 rounded-xl flex items-center justify-center shadow-lg">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white animate-pulse" />
            </div>
            <div>
              <h1 className={`font-bold text-xl ${isDark ? 'text-white' : 'text-gray-900'}`}>
                SinistrosControl
              </h1>
              <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-gray-500'}`}>
                Sistema Profissional v2.0
              </p>
            </div>
          </div>
        )}
        
        <button
          onClick={toggleSidebar}
          className={`
            p-2.5 rounded-xl transition-all duration-200 group
            ${isDark 
              ? 'hover:bg-slate-800 text-slate-400 hover:text-white' 
              : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
            }
            ${isCollapsed ? 'mx-auto' : ''}
          `}
        >
          {isCollapsed ? (
            <ChevronRight className="w-5 h-5 group-hover:scale-110 transition-transform" />
          ) : (
            <ChevronLeft className="w-5 h-5 group-hover:scale-110 transition-transform" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 overflow-y-auto custom-scrollbar">
        {menuSections.map((section, sectionIndex) => (
          <div key={section.title} className={`${sectionIndex > 0 ? 'mt-8' : ''}`}>
            {!isCollapsed && (
              <h3 className={`
                text-xs font-bold uppercase tracking-widest mb-4 px-3
                ${isDark ? 'text-slate-500' : 'text-gray-400'}
              `}>
                {section.title}
              </h3>
            )}
            <ul className="space-y-2">
              {section.items.map((item) => {
                const Icon = item.icon;
                const active = isActive(item.path);
                
                return (
                  <li key={item.path}>
                    <Link
                      to={item.path}
                      className={`
                        flex items-center p-3 rounded-xl transition-all duration-300 group relative overflow-hidden
                        ${active
                          ? `bg-gradient-to-r ${item.gradient} text-white shadow-lg shadow-${item.color.split('-')[1]}-500/25`
                          : `${isDark 
                              ? 'text-slate-300 hover:bg-slate-800/60 hover:text-white' 
                              : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                            }`
                        }
                        ${isCollapsed ? 'justify-center' : ''}
                      `}
                      title={isCollapsed ? item.label : ''}
                    >
                      {/* Background animation */}
                      {!active && (
                        <div className={`
                          absolute inset-0 bg-gradient-to-r ${item.gradient} opacity-0 
                          group-hover:opacity-10 transition-opacity duration-300
                        `} />
                      )}
                      
                      <div className="relative flex items-center w-full">
                        <Icon className={`
                          w-5 h-5 
                          ${active ? 'text-white' : item.color}
                          ${isCollapsed ? '' : 'mr-4'}
                          group-hover:scale-110 transition-transform duration-200
                        `} />
                        {!isCollapsed && (
                          <>
                            <span className="font-medium flex-1">{item.label}</span>
                            {item.badge && (
                              <span className={`
                                px-2 py-1 text-xs font-bold rounded-full
                                ${active 
                                  ? 'bg-white/20 text-white' 
                                  : 'bg-red-500 text-white'
                                }
                              `}>
                                {item.badge}
                              </span>
                            )}
                          </>
                        )}
                      </div>
                      
                      {active && !isCollapsed && (
                        <div className="absolute right-3 w-2 h-2 bg-white rounded-full opacity-80" />
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* Quick Actions */}
      {!isCollapsed && (
        <div className={`
          p-4 border-t ${isDark ? 'border-slate-700' : 'border-gray-200'}
        `}>
          <div className="space-y-3">
            <button className={`
              w-full flex items-center justify-center p-3 rounded-xl font-medium transition-all duration-300
              bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700
              shadow-lg hover:shadow-xl hover:shadow-blue-500/25 group
            `}>
              <Plus className="w-4 h-4 mr-2 group-hover:rotate-90 transition-transform duration-300" />
              Novo Sinistro
            </button>
            
            <div className="grid grid-cols-3 gap-2">
              <button className={`
                p-2.5 rounded-lg transition-colors
                ${isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'}
              `}>
                <Search className="w-4 h-4" />
              </button>
              <button className={`
                p-2.5 rounded-lg transition-colors
                ${isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'}
              `}>
                <Filter className="w-4 h-4" />
              </button>
              <button className={`
                p-2.5 rounded-lg transition-colors
                ${isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'}
              `}>
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* User Section */}
      <div className={`
        ${isDark ? 'border-slate-700 bg-slate-900/50' : 'border-gray-200 bg-gray-50/50'} 
        border-t p-4 backdrop-blur-sm
      `}>
        <div className={`
          flex items-center p-3 rounded-xl transition-colors group cursor-pointer
          ${isDark ? 'hover:bg-slate-800/60' : 'hover:bg-white/60'}
        `}>
          <div className="relative">
            <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
          </div>
          {!isCollapsed && (
            <div className="ml-3 flex-1">
              <p className={`text-sm font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Administrador
              </p>
              <p className={`text-xs ${isDark ? 'text-slate-400' : 'text-gray-500'}`}>
                Sistema Online
              </p>
            </div>
          )}
        </div>
        
        {!isCollapsed && (
          <button className={`
            w-full mt-3 flex items-center justify-center p-2.5 rounded-lg transition-colors group
            ${isDark 
              ? 'text-slate-400 hover:bg-red-500/10 hover:text-red-400' 
              : 'text-gray-600 hover:bg-red-50 hover:text-red-600'
            }
          `}>
            <LogOut className="w-4 h-4 mr-2 group-hover:scale-110 transition-transform" />
            <span className="text-sm font-medium">Sair do Sistema</span>
          </button>
        )}
      </div>
    </div>
  );
};

export default ProfessionalSidebar; 