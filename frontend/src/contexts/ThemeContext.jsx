import React, { createContext, useContext, useState, useEffect, useLayoutEffect } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [isDark, setIsDark] = useState(() => {
    // Verifica se há preferência salva
    const saved = localStorage.getItem('theme');
    if (saved) return saved === 'dark';
    
    // Se não houver, usa preferência do sistema
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  // Use useLayoutEffect para aplicar mudanças antes da renderização
  useLayoutEffect(() => {
    // Remove ou adiciona a classe de forma mais robusta
    if (isDark) {
      document.documentElement.classList.add('dark');
      document.body.classList.add('dark-mode');
    } else {
      document.documentElement.classList.remove('dark');
      document.body.classList.remove('dark-mode');
    }
    
    // Force reflow to ensure CSS updates
    void document.documentElement.offsetHeight;
    
    // Salva a preferência
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(prev => !prev);
  };

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
} 