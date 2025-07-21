// Environment configuration for the application

// Detect environment
export const isDevelopment = import.meta.env.DEV;
export const isProduction = import.meta.env.PROD;
export const isLocalhost = typeof window !== 'undefined' && 
  (window.location.hostname === 'localhost' || 
   window.location.hostname === '127.0.0.1' || 
   window.location.hostname === '::1');

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8003';

// Demo Mode Configuration
export const FORCE_DEMO_MODE = import.meta.env.VITE_DEMO_MODE === 'true';

// Auto-enable demo mode in production environments (like Vercel)
// unless a backend URL is explicitly configured
export const AUTO_DEMO_MODE = isProduction && !isLocalhost;

export const shouldUseDemoMode = () => {
  if (FORCE_DEMO_MODE) {
    console.log('🎭 Demo mode: Forced via VITE_DEMO_MODE');
    return true;
  }
  
  if (AUTO_DEMO_MODE) {
    console.log('🎭 Demo mode: Auto-enabled for production deployment');
    return true;
  }
  
  return false;
};

// App Configuration
export const APP_CONFIG = {
  name: 'Sistema de Controle de Sinistros',
  version: '2.1.0',
  demo: {
    enabled: shouldUseDemoMode(),
    timeout: 2000, // 2 seconds
    message: 'Usando dados simulados para demonstração'
  }
};