/* frontend/src/pages/SinistrosPage.jsx
 * Versão com debug e mock para teste
 */
import React, { useState, useEffect } from 'react';
import {
  AlertCircle, CheckCircle, Calendar, Filter, RefreshCw, Search,
  Eye, Truck, Edit, Save, X
} from 'lucide-react';

/**
 * Tela de gestão de sinistros com funcionalidade de edição
 */
const SinistrosPage = () => {
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
      case 'concluído':  return 'bg-green-100 text-green-800';
      case 'em análise': return 'bg-yellow-100 text-yellow-800';
      case 'pendente':   return 'bg-red-100 text-red-800';
      default:           return 'bg-gray-100 text-gray-800';
    }
  };

  const formatarMoeda = (valor) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })
      .format(valor ?? 0);

  const formatarData = (data) =>
    data ? new Date(data).toLocaleDateString('pt-BR') : '';

  const formatarDataParaInput = (data) => {
    const date = new Date(data);
    return date.toISOString().split('T')[0];
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
      const url = `http://127.0.0.1:8001/sinistros${qs ? '?' + qs : ''}`;
      
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
      
      if (data.success) {
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
    setSelectedSinistro(sinistro);
    setEditedSinistro({ ...sinistro });
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
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* ---------- Cabeçalho ------------------------------------------------ */}
        <header className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
              <AlertCircle className="text-red-600" />
              Gestão de Sinistros
            </h1>
            <p className="text-gray-600 mt-2">
              Controle e acompanhamento de ocorrências de transporte
            </p>
            {/* Debug info */}
            <div className="mt-2 text-sm text-gray-500">
              Modo: {useMock ? '🧪 Mock' : '🌐 API'} | 
              Total: {sinistros.length} sinistros
              {error && <span className="text-red-500 ml-2">⚠️ {error}</span>}
            </div>
          </div>

          <div className="flex gap-3">
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
        <div className="bg-gray-100 rounded-lg p-4 mb-6 text-sm">
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
          <section className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Filter size={20} />
              Filtros de Pesquisa
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Data inicial ------------------------------------------------ */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data Inicial
                </label>
                <input
                  type="date"
                  value={filtros.dt_ini}
                  onChange={(e) => handleFiltroChange('dt_ini', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg
                             focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Data final -------------------------------------------------- */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data Final
                </label>
                <input
                  type="date"
                  value={filtros.dt_fim}
                  onChange={(e) => handleFiltroChange('dt_fim', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg
                             focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Modal ------------------------------------------------------- */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Modal
                </label>
                <select
                  value={filtros.modal}
                  onChange={(e) => handleFiltroChange('modal', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg
                             focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Todos</option>
                  <option value="Rodoviário">Rodoviário</option>
                  <option value="Aéreo">Aéreo</option>
                </select>
              </div>

              {/* Cliente ----------------------------------------------------- */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
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
          />

          {/* Em análise ------------------------------------------------------ */}
          <Card
            label="Em Análise"
            value={sinistros.filter((s) => s.status === 'Em análise').length}
            Icon={Calendar}
            iconClass="text-yellow-600"
            valueClass="text-yellow-600"
          />

          {/* Concluídos ------------------------------------------------------ */}
          <Card
            label="Concluídos"
            value={sinistros.filter((s) => s.status === 'Concluído').length}
            Icon={CheckCircle}
            iconClass="text-green-600"
            valueClass="text-green-600"
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
          />
        </section>

        {/* ---------- Tabela -------------------------------------------------- */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">
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
                <thead className="bg-gray-50">
                  <tr>
                    <Th>Nota Fiscal</Th>
                    <Th>Conhecimento</Th>
                    <Th>Remetente</Th>
                    <Th>Destinatário</Th>
                    <Th>Data Coleta</Th>
                    <Th>Prazo Entrega</Th>
                    <Th>Data Entrega</Th>
                    <Th>Ocorrência</Th>
                    <Th>Compl. Ocorrência</Th>
                    <Th>Última Ocorrência</Th>
                    <Th>Referência</Th>
                    <Th>Data Agendamento</Th>
                    <Th>Data Ocorrência</Th>
                    <Th>Data Cadastro</Th>
                    <Th>Hora Cadastro</Th>
                    <Th>Data Alteração</Th>
                    <Th>Hora Alteração</Th>
                    <Th>Modal</Th>
                    <Th>Valor</Th>
                    <Th>Status</Th>
                    <Th>Ações</Th>
                  </tr>
                </thead>

                <tbody className="bg-white divide-y divide-gray-200">
                  {sinistros.map((s) => (
                    <tr key={`${s.nota_fiscal}-${s.nr_conhecimento}`} className="hover:bg-gray-50">
                      <Td>{s.nota_fiscal}</Td>
                      <Td bold>{s.nr_conhecimento}</Td>
                      <Td>{s.remetente}</Td>
                      <Td>{s.cliente}</Td>
                      <Td>{formatarData(s.data_coleta)}</Td>
                      <Td>{formatarData(s.prazo_entrega)}</Td>
                      <Td>{formatarData(s.data_entrega)}</Td>
                      <Td>{s.tipo_ocorrencia}</Td>
                      <Td>{s.descricao_ocorrencia}</Td>
                      <Td>{s.ultima_ocorrencia}</Td>
                      <Td>{s.referencia}</Td>
                      <Td>{formatarData(s.data_agendamento)}</Td>
                      <Td>{formatarData(s.data_evento)}</Td>
                      <Td>{formatarData(s.data_cadastro)}</Td>
                      <Td>{s.hora_cadastro}</Td>
                      <Td>{formatarData(s.data_alteracao)}</Td>
                      <Td>{s.hora_alteracao}</Td>
                      <Td>{s.modal}</Td>
                      <Td>{formatarMoeda(s.valor_mercadoria)}</Td>

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
          <Modal onClose={fecharModal}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
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
              value={editedSinistro.nr_conhecimento}
              isEditing={isEditing}
              onChange={(v) => handleEditChange('nr_conhecimento', v)}
            />

            {/* Cliente */}
            <EditableField
              label="Cliente"
              value={editedSinistro.cliente}
              isEditing={isEditing}
              onChange={(v) => handleEditChange('cliente', v)}
            />

            {/* Data do Evento */}
            <EditableField
              label="Data do Evento"
              value={
                isEditing
                  ? formatarDataParaInput(editedSinistro.data_evento)
                  : formatarData(editedSinistro.data_evento)
              }
              isEditing={isEditing}
              type={isEditing ? 'date' : 'text'}
              onChange={(v) => handleEditChange('data_evento', v)}
            />

            {/* Modal */}
            <EditableField
              label="Modal"
              value={editedSinistro.modal}
              isEditing={isEditing}
              type="select"
              options={[
                { value: 'Rodoviário', label: 'Rodoviário' },
                { value: 'Aéreo', label: 'Aéreo' },
              ]}
              onChange={(v) => handleEditChange('modal', v)}
            />

            {/* Tipo de Ocorrência */}
            <EditableField
              label="Tipo de Ocorrência"
              value={editedSinistro.tipo_ocorrencia}
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
            />

            {/* Valor da Mercadoria */}
            <EditableField
              label="Valor da Mercadoria"
              value={
                isEditing
                  ? editedSinistro.valor_mercadoria
                  : formatarMoeda(editedSinistro.valor_mercadoria)
              }
              isEditing={isEditing}
              type={isEditing ? 'number' : 'text'}
              step={isEditing ? '0.01' : undefined}
              onChange={(v) =>
                handleEditChange('valor_mercadoria', parseFloat(v) || 0)
              }
            />

            {/* Status */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              {isEditing ? (
                <select
                  value={editedSinistro.status}
                  onChange={(e) => handleEditChange('status', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg
                             focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="Pendente">Pendente</option>
                  <option value="Em análise">Em análise</option>
                  <option value="Concluído">Concluído</option>
                </select>
              ) : (
                <span
                  className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${getStatusColor(
                    editedSinistro.status
                  )}`}
                >
                  {editedSinistro.status}
                </span>
              )}
            </div>

            {/* Botões de ação */}
            {isEditing && (
              <div className="flex gap-3 mt-6 pt-4 border-t border-gray-200">
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
                  className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700
                             rounded-lg hover:bg-gray-300 transition-colors"
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
const Th = ({ children }) => (
  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
    {children}
  </th>
);

const Td = ({ children, bold = false }) => (
  <td
    className={`px-6 py-4 whitespace-nowrap text-sm ${
      bold ? 'font-medium' : ''
    } text-gray-900`}
  >
    {children}
  </td>
);

const Card = ({ label, value, Icon, iconClass = '', valueClass = '' }) => (
  <div className="bg-white rounded-lg p-6 shadow-md">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-600">{label}</p>
        <p className={`text-2xl font-bold ${valueClass}`}>{value}</p>
      </div>
      <Icon className={iconClass} size={32} />
    </div>
  </div>
);

const Modal = ({ children, onClose }) => (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div className="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
      <div className="p-6 border-b border-gray-200 flex justify-end">
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 text-xl"
        >
          ✕
        </button>
      </div>
      <div className="p-6">{children}</div>
      <div className="px-6 py-4 border-t border-gray-200 flex justify-end">
        <button
          onClick={onClose}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
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
}) => (
  <div className="mb-4">
    <label className="block text-sm font-medium text-gray-700 mb-2">
      {label}
    </label>

    {isEditing ? (
      type === 'select' ? (
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          {options.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          value={value}
          step={step}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      )
    ) : (
      <p className="text-sm text-gray-900 bg-gray-50 p-3 rounded-lg">{value}</p>
    )}
  </div>
);

export default SinistrosPage;