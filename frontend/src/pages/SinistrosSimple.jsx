import React from 'react';
import { useTheme } from '../contexts/ThemeContext';

const SinistrosSimple = () => {
  const { isDark } = useTheme();

  return (
    <div className={`min-h-screen p-8 ${isDark ? 'bg-slate-900 text-white' : 'bg-white text-gray-900'}`}>
      <h1 className="text-3xl font-bold mb-4">Teste - Página de Sinistros</h1>
      <p>Se você está vendo esta mensagem, o React Router está funcionando.</p>
      
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className={`p-4 rounded-lg ${isDark ? 'bg-slate-800' : 'bg-gray-100'}`}>
          <h3 className="font-semibold">Sinistro 1</h3>
          <p>SIN-2024-0001</p>
          <p>Status: Em análise</p>
        </div>
        <div className={`p-4 rounded-lg ${isDark ? 'bg-slate-800' : 'bg-gray-100'}`}>
          <h3 className="font-semibold">Sinistro 2</h3>
          <p>SIN-2024-0002</p>
          <p>Status: Concluído</p>
        </div>
        <div className={`p-4 rounded-lg ${isDark ? 'bg-slate-800' : 'bg-gray-100'}`}>
          <h3 className="font-semibold">Sinistro 3</h3>
          <p>SIN-2024-0003</p>
          <p>Status: Investigação</p>
        </div>
      </div>
    </div>
  );
};

export default SinistrosSimple; 