import { 
  mockSinistros, 
  mockDashboardData, 
  mockEstatisticas, 
  mockRelatorioPrejuizo, 
  simulateApiDelay 
} from './mockData.js';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8003';
const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === 'true';

// Check if backend is available
let backendAvailable = null;

const checkBackendConnection = async () => {
  if (DEMO_MODE) return false;
  
  try {
    const response = await fetch(`${API_BASE_URL}/sinistros/test/connection`, {
      method: 'GET',
      timeout: 3000 // 3 second timeout
    });
    return response.ok;
  } catch (error) {
    console.warn('Backend not available, switching to demo mode:', error.message);
    return false;
  }
};

// Wrapper function to handle API calls with fallback
const apiWithFallback = async (apiCall, fallbackData) => {
  if (backendAvailable === null) {
    backendAvailable = await checkBackendConnection();
  }
  
  if (!backendAvailable) {
    console.log('Using demo data - backend not available');
    await simulateApiDelay();
    return fallbackData;
  }
  
  try {
    return await apiCall();
  } catch (error) {
    console.warn('API call failed, falling back to demo data:', error.message);
    backendAvailable = false;
    await simulateApiDelay();
    return fallbackData;
  }
};

class SinistrosAPI {
  // Buscar todos os sinistros da query real
  static async listarSinistros(filtros = {}) {
    const apiCall = async () => {
      const params = new URLSearchParams();
      
      if (filtros.dt_ini) params.append('dt_ini', filtros.dt_ini);
      if (filtros.dt_fim) params.append('dt_fim', filtros.dt_fim);
      if (filtros.cliente) params.append('cliente', filtros.cliente);
      if (filtros.nota_fiscal) params.append('nota_fiscal', filtros.nota_fiscal);
      if (filtros.conhecimento) params.append('conhecimento', filtros.conhecimento);
      if (filtros.limit) params.append('limit', filtros.limit);
      if (filtros.page) params.append('page', filtros.page);

      const url = `${API_BASE_URL}/sinistros/sem-auth?${params.toString()}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      return await response.json();
    };

    const fallbackData = {
      sinistros: mockSinistros,
      total: mockSinistros.length,
      page: filtros.page || 1,
      limit: filtros.limit || 50,
      demo_mode: true
    };

    return await apiWithFallback(apiCall, fallbackData);
  }

  // Buscar sinistro específico
  static async obterSinistro(sinistroId) {
    try {
      // Primeiro tentar buscar por ID exato
      let response = await fetch(`${API_BASE_URL}/sinistros/sem-auth?id=${sinistroId}`);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      let result = await response.json();
      
      // Se encontrou resultados, retornar o primeiro
      if (result.sinistros && result.sinistros.length > 0) {
        return {
          success: true,
          data: result.sinistros[0] // Pegar o primeiro resultado
        };
      }
      
      // Se não encontrou por ID, tentar buscar pela nota fiscal (caso o ID seja na verdade uma nota)
      response = await fetch(`${API_BASE_URL}/sinistros/sem-auth?nota_fiscal=${sinistroId}`);
      result = await response.json();
      
      if (result.sinistros && result.sinistros.length > 0) {
        return {
          success: true,
          data: result.sinistros[0] // Pegar o primeiro resultado
        };
      }
      
      // Se não encontrou nada
      return {
        success: false,
        data: null
      };
    } catch (error) {
      console.error('Erro ao obter sinistro:', error);
      throw error;
    }
  }

  // Obter estatísticas
  static async obterEstatisticas(filtros = {}) {
    const apiCall = async () => {
      const params = new URLSearchParams();
      
      if (filtros.dt_ini) params.append('dt_ini', filtros.dt_ini);
      if (filtros.dt_fim) params.append('dt_fim', filtros.dt_fim);

      const url = `${API_BASE_URL}/sinistros/estatisticas/resumo?${params.toString()}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      return await response.json();
    };

    return await apiWithFallback(apiCall, mockEstatisticas);
  }

  // Dashboard resumo expandido
  static async obterDashboardResumo() {
    const apiCall = async () => {
      const response = await fetch(`${API_BASE_URL}/sinistros/dashboard/resumo`);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      return await response.json();
    };

    return await apiWithFallback(apiCall, mockDashboardData);
  }

  // Relatório de prejuízos
  static async obterRelatorioPrejuizo(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.dt_ini) params.append('dt_ini', filtros.dt_ini);
      if (filtros.dt_fim) params.append('dt_fim', filtros.dt_fim);
      if (filtros.setor) params.append('setor', filtros.setor);

      const url = `${API_BASE_URL}/sinistros/relatorios/prejuizo?${params.toString()}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao obter relatório de prejuízo:', error);
      throw error;
    }
  }

  // Testar conexão
  static async testarConexao() {
    const apiCall = async () => {
      const response = await fetch(`${API_BASE_URL}/sinistros/test/connection`);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      return await response.json();
    };

    const fallbackData = {
      status: "Demo Mode",
      message: "Backend não disponível. Usando dados de demonstração.",
      database_status: "Simulado",
      demo_mode: true
    };

    return await apiWithFallback(apiCall, fallbackData);
  }

  // Atualizar status de pagamento
  static async atualizarStatusPagamento(sinistroId, status, observacoes) {
    try {
      const response = await fetch(`${API_BASE_URL}/sinistros/${sinistroId}/status-pagamento`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status, observacoes })
      });
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao atualizar status de pagamento:', error);
      throw error;
    }
  }

  // Atualizar valores consolidados
  static async atualizarValores(sinistroId, valores) {
    try {
      const response = await fetch(`${API_BASE_URL}/sinistros/${sinistroId}/valores`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(valores)
      });
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao atualizar valores:', error);
      throw error;
    }
  }

  // ===== MÉTODOS PARA API DE AUTOMAÇÃO (Tabela Sinistros) =====
  
  // Obter sinistro da tabela de automação por ID
  static async obterSinistroAutomacao(sinistroId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/automacao/sinistros/${sinistroId}`);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao obter sinistro da automação:', error);
      throw error;
    }
  }

  // Obter sinistro da tabela de automação por nota fiscal
  static async obterSinistroAutomacaoPorNota(notaFiscal) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/automacao/sinistros/nota/${notaFiscal}`);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao obter sinistro da automação por nota:', error);
      throw error;
    }
  }

  // Atualizar sinistro na tabela de automação
  static async atualizarSinistroAutomacao(sinistroId, dados) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/automacao/sinistros/${sinistroId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dados)
      });
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao atualizar sinistro na automação:', error);
      throw error;
    }
  }

  // Listar sinistros da automação
  static async listarSinistrosAutomacao(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.skip) params.append('skip', filtros.skip);
      if (filtros.limit) params.append('limit', filtros.limit);
      if (filtros.status_geral) params.append('status_geral', filtros.status_geral);
      if (filtros.cliente) params.append('cliente', filtros.cliente);

      const url = `${API_BASE_URL}/api/automacao/sinistros?${params.toString()}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao buscar sinistros da automação:', error);
      throw error;
    }
  }
}

export default SinistrosAPI; 