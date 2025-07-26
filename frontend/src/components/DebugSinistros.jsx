import React, { useState, useEffect } from 'react';

const DebugSinistros = () => {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const testarAPI = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('🔧 Testando API...');
      
      const url = 'http://127.0.0.1:8001/sinistros/sem-auth?limit=5';
      console.log('📡 URL:', url);
      
      const response = await fetch(url);
      console.log('📡 Status:', response.status);
      console.log('📡 Headers:', Object.fromEntries(response.headers.entries()));
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('📦 Dados recebidos:', data);
      
      setDados(data);
      
    } catch (err) {
      console.error('❌ Erro:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    testarAPI();
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">🔧 Debug API Sinistros</h2>
      
      <button 
        onClick={testarAPI}
        className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        disabled={loading}
      >
        {loading ? 'Testando...' : 'Testar API'}
      </button>

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          <h3 className="font-bold">❌ Erro:</h3>
          <p>{error}</p>
        </div>
      )}

      {dados && (
        <div className="space-y-4">
          <div className="p-4 bg-green-100 border border-green-400 text-green-700 rounded">
            <h3 className="font-bold">✅ Sucesso!</h3>
            <p>Total de sinistros: {dados.total}</p>
            <p>Sinistros retornados: {dados.sinistros?.length || 0}</p>
            <p>Total no banco: {dados.estatisticas?.total_sinistros || 0}</p>
          </div>

          {dados.sinistros && dados.sinistros.length > 0 && (
            <div className="p-4 bg-gray-100 rounded">
              <h3 className="font-bold mb-2">📋 Primeiro Sinistro:</h3>
              <pre className="text-sm overflow-auto">
                {JSON.stringify(dados.sinistros[0], null, 2)}
              </pre>
            </div>
          )}

          <div className="p-4 bg-blue-100 rounded">
            <h3 className="font-bold mb-2">📊 Estatísticas:</h3>
            <pre className="text-sm overflow-auto">
              {JSON.stringify(dados.estatisticas, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default DebugSinistros;