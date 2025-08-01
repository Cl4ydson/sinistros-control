const API_BASE_URL = '/api';

class SinistrosAPI {
  // Buscar todos os sinistros da query real
  static async listarSinistros(filtros = {}) {
    try {
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
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao buscar sinistros:', error);
      throw error;
    }
  }

  // Buscar sinistro específico
  static async obterSinistro(sinistroId) {
    try {
      const response = await fetch(`${API_BASE_URL}/sinistros/${sinistroId}`);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao obter sinistro:', error);
      throw error;
    }
  }

  // Obter estatísticas
  static async obterEstatisticas(filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.dt_ini) params.append('dt_ini', filtros.dt_ini);
      if (filtros.dt_fim) params.append('dt_fim', filtros.dt_fim);

      const url = `${API_BASE_URL}/sinistros/estatisticas/resumo?${params.toString()}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao obter estatísticas:', error);
      throw error;
    }
  }

  // Dashboard resumo expandido
  static async obterDashboardResumo() {
    try {
      const response = await fetch(`${API_BASE_URL}/sinistros/dashboard/resumo`);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao obter dashboard:', error);
      throw error;
    }
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
    try {
      const response = await fetch(`${API_BASE_URL}/sinistros/test/connection`);
      
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao testar conexão:', error);
      throw error;
    }
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
      // Usar o endpoint correto que busca por ID (nota-conhecimento)
      const response = await fetch(`${API_BASE_URL}/api/automacao/sinistros/${notaFiscal}-${notaFiscal}`);
      
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