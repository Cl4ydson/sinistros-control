/* VERSAO DO PROJETO ANTERIOR A ETAPA DE PAGINAÇÃO

/* frontend/src/pages/SinistrosPage.jsx
 * Versão com debug e mock para teste
 */
import React, { useState, useEffect } from 'react';
import {
  AlertCircle, CheckCircle, Calendar, Filter, RefreshCw, Search,
  Eye, Truck, Edit, Save, X
} from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';
import { useTheme } from '../contexts/ThemeContext';

/**
 * Tela de gestão de sinistros com funcionalidade de edição
 */
const SinistrosPage = () => {
  /* ----------------------------------------------------------------- *
   * Theme
   * ----------------------------------------------------------------- */
  const { isDark } = useTheme();

  /* ----------------------------------------------------------------- *
   * State
   * ----------------------------------------------------------------- */
  const [sinistros,   setSinistros]   = useState([]);
  const [loading,     setLoading]     = useState(false);
  const [error,       setError]       = useState(null);
  const [showFilters, setShowFilters] = useState(false);
  const [showModal,   setShowModal]   = useState(false);
  const [selectedSinistro, setSelectedSinistro] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedSinistro, setEditedSinistro] = useState(null);
  const [useMock, setUseMock] = useState(false); // Toggle para usar mock - INICIANDO COM API REAL
  const [filtros, setFiltros] = useState({
    dt_ini : '',
    dt_fim : '',
    modal  : '',
    cliente: '',
  });

  /* ----------------------------------------------------------------- *
   * Mock Data para teste
   * ----------------------------------------------------------------- */
  const mockSinistros = [
    {
      id: 1,
      nota_fiscal: 'NF001234',
      nr_conhecimento: 'CT001234',
      remetente: 'Empresa Remetente Ltda',
      cliente: 'Cliente Destinatário SA',
      data_coleta: '2024-01-15',
      prazo_entrega: '2024-01-20',
      data_entrega: '2024-01-22',
      tipo_ocorrencia: 'Atraso',
      descricao_ocorrencia: 'Atraso na entrega devido ao trânsito',
      ultima_ocorrencia: 'Mercadoria entregue com atraso',
      referencia: 'REF-001',
      data_agendamento: '2024-01-19',
      data_evento: '2024-01-22',
      data_cadastro: '2024-01-15',
      hora_cadastro: '08:30',
      data_alteracao: '2024-01-22',
      hora_alteracao: '14:15',
      modal: 'Rodoviário',
      valor_mercadoria: 15000.50,
      status: 'Concluído'
    },
    {
      id: 2,
      nota_fiscal: 'NF001235',
      nr_conhecimento: 'CT001235',
      remetente: 'Fornecedor ABC Ltda',
      cliente: 'Empresa Compradora ME',
      data_coleta: '2024-01-16',
      prazo_entrega: '2024-01-21',
      data_entrega: null,
      tipo_ocorrencia: 'Avaria na carga',
      descricao_ocorrencia: 'Produto danificado durante transporte',
      ultima_ocorrencia: 'Aguardando perícia',
      referencia: 'REF-002',
      data_agendamento: '2024-01-20',
      data_evento: '2024-01-18',
      data_cadastro: '2024-01-16',
      hora_cadastro: '09:15',
      data_alteracao: '2024-01-18',
      hora_alteracao: '16:45',
      modal: 'Rodoviário',
      valor_mercadoria: 8500.00,
      status: 'Em análise'
    },
    {
      id: 3,
      nota_fiscal: 'NF001236',
      nr_conhecimento: 'CT001236',
      remetente: 'Industria XYZ SA',
      cliente: 'Distribuidora Nacional',
      data_coleta: '2024-01-17',
      prazo_entrega: '2024-01-19',
      data_entrega: null,
      tipo_ocorrencia: 'Furto',
      descricao_ocorrencia: 'Carga furtada durante parada',
      ultima_ocorrencia: 'Boletim de ocorrência registrado',
      referencia: 'REF-003',
      data_agendamento: null,
      data_evento: '2024-01-18',
      data_cadastro: '2024-01-17',
      hora_cadastro: '10:20',
      data_alteracao: '2024-01-18',
      hora_alteracao: '20:30',
      modal: 'Rodoviário',
      valor_mercadoria: 25000.00,
      status: 'Pendente'
    },
    {
      id: 4,
      nota_fiscal: 'NF001237',
      nr_conhecimento: 'CT001237',
      remetente: 'Empresa Aérea Ltda',
      cliente: 'Cliente Urgente SA',
      data_coleta: '2024-01-18',
      prazo_entrega: '2024-01-19',
      data_entrega: '2024-01-19',
      tipo_ocorrencia: 'Acidente',
      descricao_ocorrencia: 'Acidente durante voo, carga danificada',
      ultima_ocorrencia: 'Sinistro resolvido, indenização paga',
      referencia: 'REF-004',
      data_agendamento: '2024-01-18',
      data_evento: '2024-01-18',
      data_cadastro: '2024-01-18',
      hora_cadastro: '14:00',
      data_alteracao: '2024-01-19',
      hora_alteracao: '11:30',
      modal: 'Aéreo',
      valor_mercadoria: 45000.00,
      status: 'Concluído'
    }
  ];

  /* ----------------------------------------------------------------- *
   * Ciclo de vida
   * ----------------------------------------------------------------- */
  useEffect(() => {
    carregarSinistros();
  }, []);

  /* ----------------------------------------------------------------- *
   * Helpers
   * ----------------------------------------------------------------- */
  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'concluído':      return 'bg-green-100 text-green-800';
      case 'em andamento':   return 'bg-blue-100 text-blue-800';
      case 'não iniciado':   return 'bg-yellow-100 text-yellow-800';
      case 'não sinistrado': return 'bg-gray-100 text-gray-800';
      case 'pendente':       return 'bg-red-100 text-red-800';
      case 'em análise':     return 'bg-orange-100 text-orange-800';
      default:               return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusPagamentoColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'aguardando lançamento': return 'bg-yellow-100 text-yellow-800';
      case 'aguardando pagamento':  return 'bg-orange-100 text-orange-800';
      case 'pago':                  return 'bg-green-100 text-green-800';
      default:                      return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIndenizacaoColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'em aberto': return 'bg-red-100 text-red-800';
      case 'pago':      return 'bg-green-100 text-green-800';
      default:          return 'bg-gray-100 text-gray-800';
    }
  };

  const formatarMoeda = (valor) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })
      .format(valor ?? 0);

  const formatarData = (data) =>
    data ? new Date(data).toLocaleDateString('pt-BR') : '';

  const formatarDataParaInput = (data) => {
    if (!data) return '';
    try {
      const date = new Date(data);
      if (isNaN(date.getTime())) return '';
      return date.toISOString().split('T')[0];
    } catch (error) {
      console.error('Erro ao formatar data:', error);
      return '';
    }
  };

  /* ----------------------------------------------------------------- *
   * Handlers
   * ----------------------------------------------------------------- */
  const carregarSinistros = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('🔄 Iniciando carregamento dos sinistros...');
      console.log('📊 Usando mock:', useMock);
      
      if (useMock) {
        // Simula delay da API para teste
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log('✅ Dados mock carregados:', mockSinistros.length, 'sinistros');
        setSinistros(mockSinistros);
        return;
      }

      /* ----- monta querystring só com filtros preenchidos ------------ */
      const params = Object.fromEntries(
        Object.entries(filtros).filter(([, v]) => v)
      );
      const qs = new URLSearchParams(params).toString();
      const url = `/api/sinistros/sem-auth${qs ? '?' + qs : ''}`;
      
      console.log('🌐 Fazendo requisição para:', url);
      console.log('📋 Filtros aplicados:', params);

      /* ----- chama a API -------------------------------------------- */
      const res = await fetch(url);
      
      console.log('📡 Status da resposta:', res.status);
      console.log('📡 Headers da resposta:', Object.fromEntries(res.headers.entries()));
      
      if (!res.ok) {
        throw new Error(`API respondeu com status ${res.status}: ${res.statusText}`);
      }

      const data = await res.json();
      console.log('📦 Dados recebidos da API:', data);
      
      // Ajustar para a nova estrutura da API
      if (data.sinistros) {
        const sinistrosData = data.sinistros ?? [];
        console.log('✅ Sinistros processados:', sinistrosData.length);
        setSinistros(sinistrosData);
      } else if (data.success) {
        const sinistrosData = data.data?.sinistros ?? [];
        console.log('✅ Sinistros processados:', sinistrosData.length);
        setSinistros(sinistrosData);
      } else {
        throw new Error(data.error || 'Erro desconhecido da API');
      }

    } catch (err) {
      console.error('❌ Erro ao carregar sinistros:', err);
      console.error('❌ Stack trace:', err.stack);
      setError(`Erro ao carregar dados: ${err.message}`);
      
      // Em caso de erro, você pode optar por carregar os dados mock
      console.log('🔄 Carregando dados mock como fallback...');
      setSinistros(mockSinistros);
    } finally {
      setLoading(false);
    }
  };

  const toggleMock = () => {
    setUseMock(!useMock);
    console.log('🔧 Modo mock alterado para:', !useMock);
  };

  const handleFiltroChange = (campo, valor) => {
    console.log(`🔍 Filtro alterado - ${campo}:`, valor);
    setFiltros((prev) => ({ ...prev, [campo]: valor }));
  };

  const aplicarFiltros = () => {
    console.log('🔍 Aplicando filtros:', filtros);
    carregarSinistros();
  };

  const limparFiltros = () => {
    console.log('🧹 Limpando filtros');
    setFiltros({ dt_ini: '', dt_fim: '', modal: '', cliente: '' });
  };

  const abrirDetalhes = (sinistro) => {
    console.log('👁️ Abrindo detalhes do sinistro:', sinistro.id);
    
    // Inicializar campos adicionais se não existirem
    const sinistroCompleto = {
      ...sinistro,
      // Dados do sinistro
      obs_sinistro: sinistro.obs_sinistro || '',
      valor_sinistro: sinistro.valor_sinistro || 0,
      
      // Pagamento
      numero_nd: sinistro.numero_nd || '',
      data_vencimento_nd: sinistro.data_vencimento_nd || '',
      status_pagamento: sinistro.status_pagamento || 'Aguardando lançamento',
      
      // Indenizações
      responsavel_avaria: sinistro.responsavel_avaria || '',
      indenizado: sinistro.indenizado || 'Não',
      status_indenizacao: sinistro.status_indenizacao || 'Em aberto',
      programacao_pagamento_indenizacao: sinistro.programacao_pagamento_indenizacao || [''],
      
      // Salvados
      valor_vendido: sinistro.valor_vendido || 0,
      responsavel_compra: sinistro.responsavel_compra || '',
      programacao_pagamento_salvados: sinistro.programacao_pagamento_salvados || '',
      valor_venda: sinistro.valor_venda || 0,
      percentual_desconto: sinistro.percentual_desconto || 0,
      
      // Uso interno
      data_liberacao: sinistro.data_liberacao || '',
      responsavel_liberacao: sinistro.responsavel_liberacao || '',
      valor_liberado: sinistro.valor_liberado || 0,
      
      // Acionamento jurídico
      acionamento_juridico: sinistro.acionamento_juridico || 'Não',
      data_abertura_juridico: sinistro.data_abertura_juridico || '',
      custas_juridicas: sinistro.custas_juridicas || 0,
      
      // Acionamento seguradora
      acionamento_seguradora: sinistro.acionamento_seguradora || 'Não',
      data_abertura_seguradora: sinistro.data_abertura_seguradora || '',
      seguradora: sinistro.seguradora || '',
      programacao_indenizacao: sinistro.programacao_indenizacao || ''
    };
    
    setSelectedSinistro(sinistroCompleto);
    setEditedSinistro({ ...sinistroCompleto });
    setIsEditing(false);
    setShowModal(true);
  };

  const iniciarEdicao   = () => {
    console.log('✏️ Iniciando edição');
    setIsEditing(true);
  };
  
  const cancelarEdicao  = () => {
    console.log('❌ Cancelando edição');
    setEditedSinistro({ ...selectedSinistro }); 
    setIsEditing(false);
  };

  const handleEditChange = (campo, valor) => {
    console.log(`✏️ Campo editado - ${campo}:`, valor);
    setEditedSinistro((prev) => ({ ...prev, [campo]: valor }));
  };

  const salvarEdicao = async () => {
    try {
      console.log('💾 Salvando edição:', editedSinistro);
      
      /* ---- PUT /api/sinistros/{id}  ---------------------------------
      const res = await fetch(`/api/sinistros/${editedSinistro.id}`, {
        method : 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body   : JSON.stringify(editedSinistro)
      });
      if (!res.ok) throw new Error('Erro ao salvar');
      ---------------------------------------------------------------- */
      
      // Simula salvamento
      setSinistros((prev) =>
        prev.map((s) => (s.id === editedSinistro.id ? editedSinistro : s))
      );
      setSelectedSinistro(editedSinistro);
      setIsEditing(false);
      await new Promise((r) => setTimeout(r, 300));
      alert('Sinistro atualizado com sucesso!');
      console.log('✅ Sinistro salvo com sucesso');
    } catch (err) {
      console.error('❌ Erro ao salvar sinistro:', err);
      alert('Erro ao salvar as alterações. Tente novamente.');
    }
  };

  const fecharModal = () => {
    console.log('🚪 Fechando modal');
    setShowModal(false);
    setSelectedSinistro(null);
    setEditedSinistro(null);
    setIsEditing(false);
  };

  /* ----------------------------------------------------------------- *
   * Render
   * ----------------------------------------------------------------- */
  return (
    <div className={`min-h-screen p-6 transition-colors duration-300 ${
      isDark ? 'bg-gray-900' : 'bg-gray-50'
    }`}>
      <div className="max-w-7xl mx-auto">
                  {/* ---------- Cabeçalho ------------------------------------------------ */}
          <header className="mb-8 flex items-center justify-between">
            <div>
              <h1 className={`text-3xl font-bold flex items-center gap-3 ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>
                <AlertCircle className="text-red-600" />
                Gestão de Sinistros
              </h1>
              <p className={`mt-2 ${
                isDark ? 'text-gray-300' : 'text-gray-600'
              }`}>
                Controle e acompanhamento de ocorrências de transporte
              </p>
              {/* Debug info */}
              <div className={`mt-2 text-sm ${
                isDark ? 'text-gray-400' : 'text-gray-500'
              }`}>
                Modo: {useMock ? '🧪 Mock' : '🌐 API'} | 
                Total: {sinistros.length} sinistros
                {error && <span className="text-red-500 ml-2">⚠️ {error}</span>}
              </div>
            </div>

          <div className="flex gap-3 items-center">
            {/* Theme Toggle */}
            <ThemeToggle />

            {/* Toggle Mock */}
            <button
              onClick={toggleMock}
              className={`flex items-center gap-2 px-4 py-2 text-white rounded-lg transition-colors ${
                useMock ? 'bg-purple-600 hover:bg-purple-700' : 'bg-gray-600 hover:bg-gray-700'
              }`}
            >
              {useMock ? '🧪' : '🌐'}
              {useMock ? 'Mock' : 'API'}
            </button>

            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white
                         rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Filter size={20} />
              Filtros
            </button>

            <button
              onClick={carregarSinistros}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white
                         rounded-lg hover:bg-green-700 transition-colors"
            >
              <RefreshCw size={20} />
              Atualizar
            </button>
          </div>
        </header>

        {/* ---------- Debug Panel -------------------------------------------- */}
        <div className={`rounded-lg p-4 mb-6 text-sm ${
          isDark ? 'bg-gray-800 text-gray-200' : 'bg-gray-100 text-gray-800'
        }`}>
          <h3 className="font-semibold mb-2">🔧 Painel de Debug</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <strong>Estado:</strong> {loading ? 'Carregando...' : 'Pronto'}
            </div>
            <div>
              <strong>Sinistros:</strong> {sinistros.length}
            </div>
            <div>
              <strong>Erro:</strong> {error ? 'Sim' : 'Não'}
            </div>
            <div>
              <strong>Fonte:</strong> {useMock ? 'Mock Data' : 'API'}
            </div>
          </div>
          <div className="mt-2">
            <strong>Console:</strong> Abra o DevTools (F12) para ver logs detalhados
          </div>
        </div>

        {/* ---------- Filtros -------------------------------------------------- */}
        {showFilters && (
          <section className={`rounded-lg shadow-md p-6 mb-6 ${
            isDark ? 'bg-gray-800' : 'bg-white'
          }`}>
            <h3 className={`text-lg font-semibold mb-4 flex items-center gap-2 ${
              isDark ? 'text-white' : 'text-gray-900'
            }`}>
              <Filter size={20} />
              Filtros de Pesquisa
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Data inicial ------------------------------------------------ */}
              <div>
                <label className={`block text-sm font-medium mb-2 ${
                  isDark ? 'text-gray-300' : 'text-gray-700'
                }`}>
                  Data Inicial
                </label>
                <input
                  type="date"
                  value={filtros.dt_ini}
                  onChange={(e) => handleFiltroChange('dt_ini', e.target.value)}
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                    isDark 
                      ? 'bg-gray-700 border-gray-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                />
              </div>

              {/* Data final -------------------------------------------------- */}
              <div>
                <label className={`block text-sm font-medium mb-2 ${
                  isDark ? 'text-gray-300' : 'text-gray-700'
                }`}>
                  Data Final
                </label>
                <input
                  type="date"
                  value={filtros.dt_fim}
                  onChange={(e) => handleFiltroChange('dt_fim', e.target.value)}
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                    isDark 
                      ? 'bg-gray-700 border-gray-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                />
              </div>

              {/* Modal ------------------------------------------------------- */}
              <div>
                <label className={`block text-sm font-medium mb-2 ${
                  isDark ? 'text-gray-300' : 'text-gray-700'
                }`}>
                  Modal
                </label>
                <select
                  value={filtros.modal}
                  onChange={(e) => handleFiltroChange('modal', e.target.value)}
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                    isDark 
                      ? 'bg-gray-700 border-gray-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                >
                  <option value="">Todos</option>
                  <option value="Rodoviário">Rodoviário</option>
                  <option value="Aéreo">Aéreo</option>
                </select>
              </div>

              {/* Cliente ----------------------------------------------------- */}
              <div>
                <label className={`block text-sm font-medium mb-2 ${
                  isDark ? 'text-gray-300' : 'text-gray-700'
                }`}>
                  Cliente
                </label>
                <input
                  type="text"
                  placeholder="Nome do cliente..."
                  value={filtros.cliente}
                  onChange={(e) => handleFiltroChange('cliente', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg
                             focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Botões --------------------------------------------------------- */}
            <div className="flex gap-3 mt-4">
              <button
                onClick={aplicarFiltros}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white
                           rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Search size={16} />
                Pesquisar
              </button>

              <button
                onClick={limparFiltros}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg
                           hover:bg-gray-300 transition-colors"
              >
                Limpar
              </button>
            </div>
          </section>
        )}

        {/* ---------- Estatísticas ------------------------------------------- */}
        <section className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
          {/* Total ----------------------------------------------------------- */}
          <Card
            label="Total de Sinistros"
            value={sinistros.length}
            Icon={AlertCircle}
            iconClass="text-blue-600"
            isDark={isDark}
          />

          {/* Em análise ------------------------------------------------------ */}
          <Card
            label="Em Análise"
            value={sinistros.filter((s) => s.status === 'Em análise').length}
            Icon={Calendar}
            iconClass="text-yellow-600"
            valueClass="text-yellow-600"
            isDark={isDark}
          />

          {/* Concluídos ------------------------------------------------------ */}
          <Card
            label="Concluídos"
            value={sinistros.filter((s) => s.status === 'Concluído').length}
            Icon={CheckCircle}
            iconClass="text-green-600"
            valueClass="text-green-600"
            isDark={isDark}
          />

          {/* Valor total ----------------------------------------------------- */}
          <Card
            label="Valor Total"
            value={formatarMoeda(
              sinistros.reduce((t, s) => t + (s.valor_mercadoria ?? 0), 0)
            )}
            Icon={Truck}
            iconClass="text-red-600"
            valueClass="text-red-600"
            isDark={isDark}
          />
        </section>

        {/* ---------- Tabela -------------------------------------------------- */}
        <div className={`rounded-lg shadow-md overflow-hidden ${
          isDark ? 'bg-gray-800' : 'bg-white'
        }`}>
          <div className={`px-6 py-4 border-b ${
            isDark ? 'border-gray-700 bg-gray-800' : 'border-gray-200 bg-white'
          }`}>
            <h3 className={`text-lg font-semibold ${
              isDark ? 'text-white' : 'text-gray-900'
            }`}>
              Lista de Sinistros
            </h3>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <RefreshCw className="animate-spin mr-2" size={24} />
              <span>Carregando sinistros...</span>
            </div>
          ) : sinistros.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-gray-500">
              <AlertCircle size={48} className="mb-4" />
              <p className="text-lg">Nenhum sinistro encontrado</p>
              <p className="text-sm">
                {useMock 
                  ? 'Ative o modo API ou verifique os filtros' 
                  : 'Verifique sua conexão com a API ou ative o modo Mock para testar'
                }
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className={isDark ? 'bg-gray-700' : 'bg-gray-50'}>
                  <tr>
                    <Th isDark={isDark}>Nota Fiscal</Th>
                    <Th isDark={isDark}>Conhecimento</Th>
                    <Th isDark={isDark}>Remetente</Th>
                    <Th isDark={isDark}>Destinatário</Th>
                    <Th isDark={isDark}>Data Coleta</Th>
                    <Th isDark={isDark}>Prazo Entrega</Th>
                    <Th isDark={isDark}>Data Entrega</Th>
                    <Th isDark={isDark}>Ocorrência</Th>
                    <Th isDark={isDark}>Compl. Ocorrência</Th>
                    <Th isDark={isDark}>Última Ocorrência</Th>
                    <Th isDark={isDark}>Referência</Th>
                    <Th isDark={isDark}>Data Agendamento</Th>
                    <Th isDark={isDark}>Data Ocorrência</Th>
                    <Th isDark={isDark}>Data Cadastro</Th>
                    <Th isDark={isDark}>Hora Cadastro</Th>
                    <Th isDark={isDark}>Data Alteração</Th>
                    <Th isDark={isDark}>Hora Alteração</Th>
                    <Th isDark={isDark}>Modal</Th>
                    <Th isDark={isDark}>Valor</Th>
                    <Th isDark={isDark}>Status</Th>
                    <Th isDark={isDark}>Ações</Th>
                  </tr>
                </thead>

                <tbody className={`divide-y ${
                  isDark ? 'bg-gray-800 divide-gray-700' : 'bg-white divide-gray-200'
                }`}>
                  {sinistros.map((s) => (
                    <tr key={`${s.nota_fiscal}-${s.nr_conhecimento}`} className={
                      isDark ? 'hover:bg-gray-700' : 'hover:bg-gray-50'
                    }>
                      <Td isDark={isDark}>{s.nota_fiscal}</Td>
                      <Td bold isDark={isDark}>{s.nr_conhecimento}</Td>
                      <Td isDark={isDark}>{s.remetente}</Td>
                      <Td isDark={isDark}>{s.cliente}</Td>
                      <Td isDark={isDark}>{formatarData(s.data_coleta)}</Td>
                      <Td isDark={isDark}>{formatarData(s.prazo_entrega)}</Td>
                      <Td isDark={isDark}>{formatarData(s.data_entrega)}</Td>
                      <Td isDark={isDark}>{s.tipo_ocorrencia}</Td>
                      <Td isDark={isDark}>{s.descricao_ocorrencia}</Td>
                      <Td isDark={isDark}>{s.ultima_ocorrencia}</Td>
                      <Td isDark={isDark}>{s.referencia}</Td>
                      <Td isDark={isDark}>{formatarData(s.data_agendamento)}</Td>
                      <Td isDark={isDark}>{formatarData(s.data_evento)}</Td>
                      <Td isDark={isDark}>{formatarData(s.data_cadastro)}</Td>
                      <Td isDark={isDark}>{s.hora_cadastro}</Td>
                      <Td isDark={isDark}>{formatarData(s.data_alteracao)}</Td>
                      <Td isDark={isDark}>{s.hora_alteracao}</Td>
                      <Td isDark={isDark}>{s.modal}</Td>
                      <Td isDark={isDark}>{formatarMoeda(s.valor_mercadoria)}</Td>

                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`inline-flex px-2 py-1 text-xs font-semibold
                                      rounded-full ${getStatusColor(s.status)}`}
                        >
                          {s.status}
                        </span>
                      </td>

                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => abrirDetalhes(s)}
                          className="text-blue-600 hover:text-blue-900 flex items-center gap-1"
                        >
                          <Eye size={16} />
                          Ver
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* ---------- Modal --------------------------------------------------- */}
        {showModal && selectedSinistro && editedSinistro && (
          <Modal onClose={fecharModal} isDark={isDark}>
            <div className="flex items-center justify-between mb-6">
              <h2 className={`text-xl font-semibold ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>
                {isEditing ? 'Editar Sinistro' : 'Detalhes do Sinistro'}
              </h2>

              {!isEditing && (
                <button
                  onClick={iniciarEdicao}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white
                             rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Edit size={16} />
                  Editar
                </button>
              )}
            </div>

            {/* Número do Conhecimento */}
            <EditableField
              label="Número do Conhecimento"
              value={editedSinistro?.nr_conhecimento || ''}
              isEditing={isEditing}
              onChange={(v) => handleEditChange('nr_conhecimento', v)}
              isDark={isDark}
            />

            {/* Cliente */}
            <EditableField
              label="Cliente"
              value={editedSinistro?.cliente || ''}
              isEditing={isEditing}
              onChange={(v) => handleEditChange('cliente', v)}
              isDark={isDark}
            />

            {/* Data do Evento */}
            <EditableField
              label="Data do Evento"
              value={
                isEditing
                  ? formatarDataParaInput(editedSinistro?.data_evento)
                  : formatarData(editedSinistro?.data_evento)
              }
              isEditing={isEditing}
              type={isEditing ? 'date' : 'text'}
              onChange={(v) => handleEditChange('data_evento', v)}
              isDark={isDark}
            />

            {/* Modal */}
            <EditableField
              label="Modal"
              value={editedSinistro?.modal || ''}
              isEditing={isEditing}
              type="select"
              options={[
                { value: 'Rodoviário', label: 'Rodoviário' },
                { value: 'Aéreo', label: 'Aéreo' },
              ]}
              onChange={(v) => handleEditChange('modal', v)}
              isDark={isDark}
            />

            {/* Tipo de Ocorrência */}
            <EditableField
              label="Tipo de Ocorrência"
              value={editedSinistro?.tipo_ocorrencia || ''}
              isEditing={isEditing}
              type="select"
              options={[
                { value: 'Avaria na carga', label: 'Avaria na carga' },
                { value: 'Furto', label: 'Furto' },
                { value: 'Acidente', label: 'Acidente' },
                { value: 'Perda total', label: 'Perda total' },
                { value: 'Atraso', label: 'Atraso' },
              ]}
              onChange={(v) => handleEditChange('tipo_ocorrencia', v)}
              isDark={isDark}
            />

            {/* Valor da Mercadoria */}
            <EditableField
              label="Valor da Mercadoria"
              value={
                isEditing
                  ? editedSinistro?.valor_mercadoria || 0
                  : formatarMoeda(editedSinistro?.valor_mercadoria || 0)
              }
              isEditing={isEditing}
              type={isEditing ? 'number' : 'text'}
              step={isEditing ? '0.01' : undefined}
              onChange={(v) =>
                handleEditChange('valor_mercadoria', parseFloat(v) || 0)
              }
              isDark={isDark}
            />

            {/* Status */}
            <div className="mb-4">
              <label className={`block text-sm font-medium mb-2 ${
                isDark ? 'text-gray-300' : 'text-gray-700'
              }`}>
                Status
              </label>
              {isEditing ? (
                <select
                  value={editedSinistro?.status || 'Não iniciado'}
                  onChange={(e) => handleEditChange('status', e.target.value)}
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                    isDark 
                      ? 'bg-gray-700 border-gray-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                >
                  <option value="Não iniciado">Não iniciado</option>
                  <option value="Em andamento">Em andamento</option>
                  <option value="Concluído">Concluído</option>
                  <option value="Não sinistrado">Não sinistrado</option>
                </select>
              ) : (
                <span
                  className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${getStatusColor(
                    editedSinistro?.status
                  )}`}
                >
                  {editedSinistro?.status || 'Não iniciado'}
                </span>
              )}
            </div>

            {/* ==================== DADOS DO SINISTRO ==================== */}
            <div className={`border-t my-6 pt-6 ${
              isDark ? 'border-gray-600' : 'border-gray-300'
            }`}>
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>Dados do Sinistro</h3>
              
              {/* Observações */}
              <EditableField
                label="Observações"
                value={editedSinistro?.obs_sinistro || ''}
                isEditing={isEditing}
                type="textarea"
                onChange={(v) => handleEditChange('obs_sinistro', v)}
                isDark={isDark}
              />

              {/* Valor do Sinistro */}
              <EditableField
                label="Valor do Sinistro"
                value={
                  isEditing
                    ? editedSinistro?.valor_sinistro || 0
                    : formatarMoeda(editedSinistro?.valor_sinistro || 0)
                }
                isEditing={isEditing}
                type={isEditing ? 'number' : 'text'}
                step={isEditing ? '0.01' : undefined}
                onChange={(v) => handleEditChange('valor_sinistro', parseFloat(v) || 0)}
                isDark={isDark}
              />
            </div>

            {/* ==================== PAGAMENTO ==================== */}
            <div className={`border-t my-6 pt-6 ${
              isDark ? 'border-gray-600' : 'border-gray-300'
            }`}>
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>Pagamento</h3>
              
              {/* Número ND */}
              <EditableField
                label="N° ND"
                value={editedSinistro?.numero_nd || ''}
                isEditing={isEditing}
                onChange={(v) => handleEditChange('numero_nd', v)}
                isDark={isDark}
              />

              {/* Data Vencimento ND */}
              <EditableField
                label="Data Vencimento ND"
                value={
                  isEditing
                    ? formatarDataParaInput(editedSinistro?.data_vencimento_nd)
                    : formatarData(editedSinistro?.data_vencimento_nd)
                }
                isEditing={isEditing}
                type={isEditing ? 'date' : 'text'}
                onChange={(v) => handleEditChange('data_vencimento_nd', v)}
                isDark={isDark}
              />

              {/* Status do Pagamento */}
              <div className="mb-4">
                <label className={`block text-sm font-medium mb-2 ${
                  isDark ? 'text-gray-300' : 'text-gray-700'
                }`}>
                  Status do Pagamento
                </label>
                {isEditing ? (
                  <select
                    value={editedSinistro?.status_pagamento || 'Aguardando lançamento'}
                    onChange={(e) => handleEditChange('status_pagamento', e.target.value)}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                      isDark 
                        ? 'bg-gray-700 border-gray-600 text-white' 
                        : 'bg-white border-gray-300 text-gray-900'
                    }`}
                  >
                    <option value="Aguardando lançamento">Aguardando lançamento</option>
                    <option value="Aguardando Pagamento">Aguardando Pagamento</option>
                    <option value="Pago">Pago</option>
                  </select>
                ) : (
                  <span
                    className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${getStatusPagamentoColor(
                      editedSinistro?.status_pagamento
                    )}`}
                  >
                    {editedSinistro?.status_pagamento || 'Aguardando lançamento'}
                  </span>
                )}
              </div>
            </div>

            {/* ==================== INDENIZAÇÕES ==================== */}
            <div className={`border-t my-6 pt-6 ${
              isDark ? 'border-gray-600' : 'border-gray-300'
            }`}>
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>Indenizações</h3>
              
              {/* Responsável pela Avaria */}
              <EditableField
                label="Responsável pela Avaria"
                value={editedSinistro?.responsavel_avaria || ''}
                isEditing={isEditing}
                type="select"
                options={[
                  { value: '', label: 'Selecione...' },
                  { value: 'Transportadora', label: 'Transportadora' },
                  { value: 'Seguradora', label: 'Seguradora' },
                  { value: 'Terceiros', label: 'Terceiros' },
                  { value: 'Cliente', label: 'Cliente' },
                  { value: 'Outros', label: 'Outros' }
                ]}
                onChange={(v) => handleEditChange('responsavel_avaria', v)}
                isDark={isDark}
              />

              {/* Indenizado */}
              <EditableField
                label="Indenizado?"
                value={editedSinistro?.indenizado || 'Não'}
                isEditing={isEditing}
                type="select"
                options={[
                  { value: 'Não', label: 'Não' },
                  { value: 'Sim', label: 'Sim' }
                ]}
                onChange={(v) => handleEditChange('indenizado', v)}
                isDark={isDark}
              />

              {/* Status da Indenização */}
              <div className="mb-4">
                <label className={`block text-sm font-medium mb-2 ${
                  isDark ? 'text-gray-300' : 'text-gray-700'
                }`}>
                  Status da Indenização
                </label>
                {isEditing ? (
                  <select
                    value={editedSinistro?.status_indenizacao || 'Em aberto'}
                    onChange={(e) => handleEditChange('status_indenizacao', e.target.value)}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                      isDark 
                        ? 'bg-gray-700 border-gray-600 text-white' 
                        : 'bg-white border-gray-300 text-gray-900'
                    }`}
                  >
                    <option value="Em aberto">Em aberto</option>
                    <option value="Pago">Pago</option>
                  </select>
                ) : (
                  <span
                    className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${getStatusIndenizacaoColor(
                      editedSinistro?.status_indenizacao
                    )}`}
                  >
                    {editedSinistro?.status_indenizacao || 'Em aberto'}
                  </span>
                )}
              </div>

              {/* Programação de Pagamento (apenas se indenizado = Sim) */}
              {editedSinistro?.indenizado === 'Sim' && (
                <ProgramacaoPagamento
                  label="Programação de Pagamento (até 10 datas)"
                  values={editedSinistro.programacao_pagamento_indenizacao || ['']}
                  isEditing={isEditing}
                  onChange={(v) => handleEditChange('programacao_pagamento_indenizacao', v)}
                  isDark={isDark}
                />
              )}
            </div>

            {/* ==================== SALVADOS ==================== */}
            <div className={`border-t my-6 pt-6 ${
              isDark ? 'border-gray-600' : 'border-gray-300'
            }`}>
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>Salvados</h3>
              
              {/* Valor Vendido */}
              <EditableField
                label="Valor Vendido"
                value={
                  isEditing
                    ? editedSinistro?.valor_vendido || 0
                    : formatarMoeda(editedSinistro?.valor_vendido || 0)
                }
                isEditing={isEditing}
                type={isEditing ? 'number' : 'text'}
                step={isEditing ? '0.01' : undefined}
                onChange={(v) => handleEditChange('valor_vendido', parseFloat(v) || 0)}
              isDark={isDark}
              />

              {/* Responsável pela Compra */}
              <EditableField
                label="Responsável pela Compra"
                value={editedSinistro?.responsavel_compra || ''}
                isEditing={isEditing}
                onChange={(v) => handleEditChange('responsavel_compra', v)}
                isDark={isDark}
              />

              {/* Programação de Pagamento */}
              <EditableField
                label="Programação de Pagamento"
                value={editedSinistro?.programacao_pagamento_salvados || ''}
                isEditing={isEditing}
                onChange={(v) => handleEditChange('programacao_pagamento_salvados', v)}
                isDark={isDark}
              />

              {/* Valor da Venda */}
              <EditableField
                label="Valor da Venda"
                value={
                  isEditing
                    ? editedSinistro?.valor_venda || 0
                    : formatarMoeda(editedSinistro?.valor_venda || 0)
                }
                isEditing={isEditing}
                type={isEditing ? 'number' : 'text'}
                step={isEditing ? '0.01' : undefined}
                onChange={(v) => handleEditChange('valor_venda', parseFloat(v) || 0)}
                isDark={isDark}
              />

              {/* Percentual de Desconto */}
              <EditableField
                label="% de Desconto"
                value={editedSinistro?.percentual_desconto || 0}
                isEditing={isEditing}
                type="number"
                step="0.01"
                onChange={(v) => handleEditChange('percentual_desconto', parseFloat(v) || 0)}
                isDark={isDark}
              />
            </div>

            {/* ==================== USO INTERNO ==================== */}
            <div className={`border-t my-6 pt-6 ${
              isDark ? 'border-gray-600' : 'border-gray-300'
            }`}>
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>Uso Interno</h3>
              
              {/* Data da Liberação */}
              <EditableField
                label="Data da Liberação"
                value={
                  isEditing
                    ? formatarDataParaInput(editedSinistro?.data_liberacao)
                    : formatarData(editedSinistro?.data_liberacao)
                }
                isEditing={isEditing}
                type={isEditing ? 'date' : 'text'}
                onChange={(v) => handleEditChange('data_liberacao', v)}
                isDark={isDark}
              />

              {/* Responsável pela Liberação */}
              <EditableField
                label="Responsável pela Liberação"
                value={editedSinistro?.responsavel_liberacao || ''}
                isEditing={isEditing}
                onChange={(v) => handleEditChange('responsavel_liberacao', v)}
                isDark={isDark}
              />

              {/* Valor Liberado */}
              <EditableField
                label="Valor Liberado"
                value={
                  isEditing
                    ? editedSinistro?.valor_liberado || 0
                    : formatarMoeda(editedSinistro?.valor_liberado || 0)
                }
                isEditing={isEditing}
                type={isEditing ? 'number' : 'text'}
                step={isEditing ? '0.01' : undefined}
                onChange={(v) => handleEditChange('valor_liberado', parseFloat(v) || 0)}
                isDark={isDark}
              />
            </div>

            {/* ==================== ACIONAMENTO JURÍDICO ==================== */}
            <div className={`border-t my-6 pt-6 ${
              isDark ? 'border-gray-600' : 'border-gray-300'
            }`}>
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>Acionamento Jurídico</h3>
              
              {/* Acionamento Jurídico */}
              <EditableField
                label="Acionamento Jurídico?"
                value={editedSinistro?.acionamento_juridico || 'Não'}
                isEditing={isEditing}
                type="select"
                options={[
                  { value: 'Não', label: 'Não' },
                  { value: 'Sim', label: 'Sim' }
                ]}
                onChange={(v) => handleEditChange('acionamento_juridico', v)}
                isDark={isDark}
              />

              {/* Campos adicionais se acionamento jurídico = Sim */}
              {editedSinistro?.acionamento_juridico === 'Sim' && (
                <>
                                      <EditableField
                      label="Data de Abertura do Sinistro"
                      value={
                        isEditing
                          ? formatarDataParaInput(editedSinistro?.data_abertura_juridico)
                          : formatarData(editedSinistro?.data_abertura_juridico)
                      }
                      isEditing={isEditing}
                      type={isEditing ? 'date' : 'text'}
                      onChange={(v) => handleEditChange('data_abertura_juridico', v)}
                      isDark={isDark}
                    />

                    <EditableField
                      label="Custas Jurídicas"
                      value={
                        isEditing
                          ? editedSinistro?.custas_juridicas || 0
                          : formatarMoeda(editedSinistro?.custas_juridicas || 0)
                      }
                      isEditing={isEditing}
                      type={isEditing ? 'number' : 'text'}
                      step={isEditing ? '0.01' : undefined}
                      onChange={(v) => handleEditChange('custas_juridicas', parseFloat(v) || 0)}
                      isDark={isDark}
                    />
                </>
              )}
            </div>

            {/* ==================== ACIONAMENTO SEGURADORA ==================== */}
            <div className={`border-t my-6 pt-6 ${
              isDark ? 'border-gray-600' : 'border-gray-300'
            }`}>
              <h3 className={`text-lg font-semibold mb-4 ${
                isDark ? 'text-white' : 'text-gray-900'
              }`}>Acionamento Seguradora</h3>
              
              {/* Acionamento Seguradora */}
              <EditableField
                label="Acionamento Seguradora?"
                value={editedSinistro?.acionamento_seguradora || 'Não'}
                isEditing={isEditing}
                type="select"
                options={[
                  { value: 'Não', label: 'Não' },
                  { value: 'Sim', label: 'Sim' }
                ]}
                onChange={(v) => handleEditChange('acionamento_seguradora', v)}
                isDark={isDark}
              />

              {/* Campos adicionais se acionamento seguradora = Sim */}
              {editedSinistro?.acionamento_seguradora === 'Sim' && (
                <>
                  <EditableField
                    label="Data de Abertura do Sinistro"
                    value={
                      isEditing
                        ? formatarDataParaInput(editedSinistro?.data_abertura_seguradora)
                        : formatarData(editedSinistro?.data_abertura_seguradora)
                    }
                    isEditing={isEditing}
                    type={isEditing ? 'date' : 'text'}
                    onChange={(v) => handleEditChange('data_abertura_seguradora', v)}
                    isDark={isDark}
                  />

                  <EditableField
                    label="Seguradora"
                    value={editedSinistro?.seguradora || ''}
                    isEditing={isEditing}
                    onChange={(v) => handleEditChange('seguradora', v)}
                    isDark={isDark}
                  />

                  <EditableField
                    label="Programação de Indenização"
                    value={editedSinistro?.programacao_indenizacao || ''}
                    isEditing={isEditing}
                    onChange={(v) => handleEditChange('programacao_indenizacao', v)}
                    isDark={isDark}
                  />
                </>
              )}
            </div>

            {/* Botões de ação */}
            {isEditing && (
              <div className={`flex gap-3 mt-6 pt-4 border-t ${
                isDark ? 'border-gray-600' : 'border-gray-200'
              }`}>
                <button
                  onClick={salvarEdicao}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white
                             rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Save size={16} />
                  Salvar
                </button>

                <button
                  onClick={cancelarEdicao}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                    isDark 
                      ? 'bg-gray-700 text-gray-300 hover:bg-gray-600' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  <X size={16} />
                  Cancelar
                </button>
              </div>
            )}
          </Modal>
        )}
      </div>
    </div>
  );
};

/* --------------------------------------------------------------------- *
 * Componentes auxiliares
 * --------------------------------------------------------------------- */
const Th = ({ children, isDark = false }) => (
  <th className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider ${
    isDark ? 'text-gray-300' : 'text-gray-500'
  }`}>
    {children}
  </th>
);

const Td = ({ children, bold = false, isDark = false }) => (
  <td
    className={`px-6 py-4 whitespace-nowrap text-sm ${
      bold ? 'font-medium' : ''
    } ${isDark ? 'text-gray-200' : 'text-gray-900'}`}
  >
    {children}
  </td>
);

const Card = ({ label, value, Icon, iconClass = '', valueClass = '', isDark = false }) => (
  <div className={`rounded-lg p-6 shadow-md ${
    isDark ? 'bg-gray-800' : 'bg-white'
  }`}>
    <div className="flex items-center justify-between">
      <div>
        <p className={`text-sm ${
          isDark ? 'text-gray-400' : 'text-gray-600'
        }`}>{label}</p>
        <p className={`text-2xl font-bold ${valueClass} ${
          isDark && !valueClass ? 'text-white' : ''
        }`}>{value}</p>
      </div>
      <Icon className={iconClass} size={32} />
    </div>
  </div>
);

const Modal = ({ children, onClose, isDark = false }) => (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div className={`rounded-lg max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto ${
      isDark ? 'bg-gray-800' : 'bg-white'
    }`}>
      <div className={`p-6 border-b flex justify-end ${
        isDark ? 'border-gray-700' : 'border-gray-200'
      }`}>
        <button
          onClick={onClose}
          className={`text-xl ${
            isDark ? 'text-gray-400 hover:text-gray-200' : 'text-gray-400 hover:text-gray-600'
          }`}
        >
          ✕
        </button>
      </div>
      <div className="p-6">{children}</div>
      <div className={`px-6 py-4 border-t flex justify-end ${
        isDark ? 'border-gray-700' : 'border-gray-200'
      }`}>
        <button
          onClick={onClose}
          className={`px-4 py-2 rounded-lg transition-colors ${
            isDark 
              ? 'bg-gray-700 text-gray-300 hover:bg-gray-600' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Fechar
        </button>
      </div>
    </div>
  </div>
);

const EditableField = ({
  label,
  value,
  isEditing,
  type = 'text',
  options = [],
  onChange,
  step,
  isDark = false,
}) => (
  <div className="mb-4">
    <label className={`block text-sm font-medium mb-2 ${
      isDark ? 'text-gray-300' : 'text-gray-700'
    }`}>
      {label}
    </label>

    {isEditing ? (
      type === 'select' ? (
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
            isDark 
              ? 'bg-gray-700 border-gray-600 text-white' 
              : 'bg-white border-gray-300 text-gray-900'
          }`}
        >
          {options.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      ) : type === 'textarea' ? (
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          rows={4}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
            isDark 
              ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
              : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
          }`}
        />
      ) : (
        <input
          type={type}
          value={value}
          step={step}
          onChange={(e) => onChange(e.target.value)}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
            isDark 
              ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
              : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
          }`}
        />
      )
    ) : (
      <p className={`text-sm p-3 rounded-lg ${
        isDark 
          ? 'text-gray-200 bg-gray-700' 
          : 'text-gray-900 bg-gray-50'
      }`}>{value}</p>
    )}
  </div>
);

const ProgramacaoPagamento = ({ label, values = [''], isEditing, onChange, isDark = false }) => {
  const formatarDataLocal = (data) =>
    data ? new Date(data).toLocaleDateString('pt-BR') : '';

  const formatarDataCompleta = (data) => {
    if (!data) return '';
    const date = new Date(data);
    return date.toLocaleDateString('pt-BR', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const getDiasRestantes = (data) => {
    if (!data) return null;
    const hoje = new Date();
    const dataTarget = new Date(data);
    const diffTime = dataTarget - hoje;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  const getStatusData = (data) => {
    const dias = getDiasRestantes(data);
    if (dias === null) return { color: 'bg-gray-100 text-gray-800', text: '' };
    if (dias < 0) return { color: 'bg-red-100 text-red-800', text: `${Math.abs(dias)} dias em atraso` };
    if (dias === 0) return { color: 'bg-yellow-100 text-yellow-800', text: 'Hoje' };
    if (dias <= 7) return { color: 'bg-orange-100 text-orange-800', text: `${dias} dias` };
    return { color: 'bg-green-100 text-green-800', text: `${dias} dias` };
  };

  // Garantir que values é sempre um array
  const safeValues = Array.isArray(values) ? values : [''];

  const addData = () => {
    if (safeValues.length < 10) {
      onChange([...safeValues, '']);
    }
  };

  const removeData = (index) => {
    onChange(safeValues.filter((_, i) => i !== index));
  };

  const updateData = (index, value) => {
    const newValues = [...safeValues];
    newValues[index] = value;
    onChange(newValues);
  };

  return (
    <div className="mb-4">
      <label className={`block text-sm font-medium mb-2 ${
        isDark ? 'text-gray-300' : 'text-gray-700'
      }`}>
        {label}
      </label>
      
      {isEditing ? (
        <div className="space-y-2">
          {safeValues.map((data, index) => (
            <div key={index} className="flex gap-2">
              <input
                type="date"
                value={data}
                onChange={(e) => updateData(index, e.target.value)}
                className={`flex-1 px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  isDark 
                    ? 'bg-gray-700 border-gray-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-900'
                }`}
              />
              {safeValues.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeData(index)}
                  className="px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                >
                  ✕
                </button>
              )}
            </div>
          ))}
          
          {safeValues.length < 10 && (
            <button
              type="button"
              onClick={addData}
              className="px-3 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              + Adicionar Data
            </button>
          )}
        </div>
      ) : (
        <div className={`p-3 rounded-lg ${
          isDark ? 'bg-gray-700' : 'bg-gray-50'
        }`}>
          {safeValues.filter(v => v).length > 0 ? (
            <div className="space-y-3">
              {safeValues.filter(v => v).map((data, index) => {
                const status = getStatusData(data);
                return (
                  <div key={index} className={`flex items-center justify-between p-3 rounded-lg border shadow-sm ${
                    isDark 
                      ? 'bg-gray-800 border-gray-600' 
                      : 'bg-white border-gray-200'
                  }`}>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className={`flex items-center justify-center w-6 h-6 text-xs font-bold rounded-full ${
                          isDark 
                            ? 'bg-blue-600 text-blue-100' 
                            : 'bg-blue-100 text-blue-800'
                        }`}>
                          {index + 1}
                        </span>
                        <div>
                          <p className={`text-sm font-semibold ${
                            isDark ? 'text-gray-200' : 'text-gray-900'
                          }`}>
                            {formatarDataLocal(data)}
                          </p>
                          <p className={`text-xs ${
                            isDark ? 'text-gray-400' : 'text-gray-500'
                          }`}>
                            {formatarDataCompleta(data)}
                          </p>
                        </div>
                      </div>
                    </div>
                    {status.text && (
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${status.color}`}>
                        {status.text}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <p className={`text-sm text-center py-4 ${
              isDark ? 'text-gray-400' : 'text-gray-500'
            }`}>
              📅 Nenhuma data programada
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default SinistrosPage;