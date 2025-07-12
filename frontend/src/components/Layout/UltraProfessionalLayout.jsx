import React, { useState, useEffect } from 'react';
import ProfessionalSidebar from './ProfessionalSidebar';
import ProfessionalHeader from './ProfessionalHeader';
import { useTheme } from '../../contexts/ThemeContext';

const UltraProfessionalLayout = ({ 
  children, 
  title, 
  subtitle,
  breadcrumbs = [],
  showSearch = true,
  headerActions = []
}) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const { isDark } = useTheme();

  // Detect mobile screen and auto-collapse sidebar
  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth < 1024;
      setIsMobile(mobile);
      if (mobile) {
        setSidebarCollapsed(true);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <div className={`
      min-h-screen relative
      ${isDark 
        ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900' 
        : 'bg-gradient-to-br from-gray-50 via-white to-gray-100'
      }
    `}>
      {/* Background Pattern */}
      <div className="fixed inset-0 pointer-events-none">
        <div className={`
          absolute inset-0 opacity-5
          ${isDark ? 'bg-slate-400' : 'bg-gray-600'}
        `} 
        style={{
          backgroundImage: `radial-gradient(circle at 25% 25%, currentColor 2px, transparent 2px),
                           radial-gradient(circle at 75% 75%, currentColor 2px, transparent 2px)`,
          backgroundSize: '50px 50px'
        }} />
      </div>

      {/* Professional Sidebar */}
      <ProfessionalSidebar 
        isCollapsed={sidebarCollapsed} 
        toggleSidebar={toggleSidebar} 
      />

      {/* Main Content Area */}
      <div className={`
        transition-all duration-300 relative z-10
        ${sidebarCollapsed ? (isMobile ? 'ml-0' : 'ml-20') : (isMobile ? 'ml-0' : 'ml-72')}
      `}>
        {/* Professional Header */}
        <ProfessionalHeader 
          title={title}
          subtitle={subtitle}
          breadcrumbs={breadcrumbs}
          onToggleSidebar={toggleSidebar}
          showSearch={showSearch}
          actions={headerActions}
        />

        {/* Page Content Container */}
        <main className="relative">
          {/* Content Background */}
          <div className={`
            min-h-[calc(100vh-80px)] p-6
            ${isDark 
              ? 'bg-gradient-to-b from-transparent to-slate-900/20' 
              : 'bg-gradient-to-b from-transparent to-gray-50/20'
            }
          `}>
            {/* Glass Effect Container */}
            <div className={`
              rounded-2xl backdrop-blur-sm border min-h-full
              ${isDark 
                ? 'bg-slate-900/40 border-slate-700/50' 
                : 'bg-white/40 border-gray-200/50'
              }
              shadow-2xl shadow-black/5
            `}>
              <div className="p-8">
                {children}
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Mobile Overlay */}
      {isMobile && !sidebarCollapsed && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          onClick={toggleSidebar}
        />
      )}

      {/* Floating Action Button for Mobile */}
      {isMobile && sidebarCollapsed && (
        <button
          onClick={toggleSidebar}
          className={`
            fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-2xl z-50
            bg-gradient-to-r from-blue-600 to-purple-600 text-white
            hover:from-blue-700 hover:to-purple-700 transition-all duration-300
            hover:scale-110 active:scale-95
          `}
        >
          <svg className="w-6 h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      )}

      {/* Custom Scrollbar Styles */}
      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: ${isDark ? '#1e293b' : '#f1f5f9'};
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: ${isDark ? '#475569' : '#cbd5e1'};
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: ${isDark ? '#64748b' : '#94a3b8'};
        }
      `}</style>
    </div>
  );
};

export default UltraProfessionalLayout; 