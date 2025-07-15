import React from 'react';
import DebugSinistros from '../components/DebugSinistros';

const TestePage = () => {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">🧪 Página de Teste</h1>
        <DebugSinistros />
      </div>
    </div>
  );
};

export default TestePage;