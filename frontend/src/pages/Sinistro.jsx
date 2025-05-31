import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, Calendar, Filter, RefreshCw, Search, Eye, Truck, Edit, Save, X } from 'lucide-react';

/**
 * Tela de gestão de sinistros com funcionalidade de edição
 */
const SinistrosPage = () => {
  /* ----------------------------------------------------------------- *
   * State
   * ----------------------------------------------------------------- */
  const [sinistros,   setSinistros]   = useState([]);
  const [loading,     setLoading]     = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [showModal,   setShowModal]   = useState(false);
  const [selectedSinistro, setSelectedSinistro] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedSinistro, setEditedSinistro] = useState(null);
  const [filtros, setFiltros] = useState({
    dt_ini: '',
    dt_fim: '',
    modal : '',
    cliente: ''
  });

  /* ----------------------------------------------------------------- *
   * Mock - remover quando integrar à API real
   * ----------------------------------------------------------------- */
  const mockSinistros = [
    {
      id: 1,
      nr_conhecimento : 'CTR001234',
      cliente         : 'Empresa ABC Ltda',
      data_evento     : '2024-05-15',
      modal           : 'Rodoviário',
      tipo_ocorrencia : 'Avaria na carga',
      valor_mercadoria: 15000.5,
      status          : 'Em análise'
    },
    {
      id: 2,
      nr_conhecimento : 'CTR001235',
      cliente         : 'Comércio XYZ S.A.',
      data_evento     : '2024-05-20',
      modal           : 'Aéreo',
      tipo_ocorrencia : 'Furto',
      valor_mercadoria: 25000.0,
      status          : 'Concluído'
    },
    {
      id: 3,
      nr_conhecimento : 'CTR001236',
      cliente         : 'Indústria 123',
      data_evento     : '2024-05-25',
      modal           : 'Aéreo',
      tipo_ocorrencia : 'Acidente',
      valor_mercadoria: 45000.75,
      status          : 'Pendente'
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
    new Date(data).toLocaleDateString('pt-BR');

  const formatarDataParaInput = (data) => {
    // Converte data para formato YYYY-MM-DD para inputs do tipo date
    const date = new Date(data);
    return date.toISOString().split('T')[0];
  };

  /* ----------------------------------------------------------------- *
   * Handlers
   * ----------------------------------------------------------------- */
  const carregarSinistros = async () => {
    setLoading(true);

    try {
      // 👉  produção:
      // const res  = await fetch('/api/sinistros?' + new URLSearchParams(filtros));
      // const data = await res.json();
      // setSinistros(data);

      // 👉  mock:
      setTimeout(() => {
        setSinistros(mockSinistros);
        setLoading(false);
      }, 1000);
    } catch (err) {
      console.error('Erro ao carregar sinistros:', err);
      setLoading(false);
    }
  };

  const handleFiltroChange = (campo, valor) =>
    setFiltros((prev) => ({ ...prev, [campo]: valor }));

  const aplicarFiltros = () => carregarSinistros();

  const limparFiltros = () =>
    setFiltros({ dt_ini: '', dt_fim: '', modal: '', cliente: '' });

  const abrirDetalhes = (sinistro) => {
    setSelectedSinistro(sinistro);
    setEditedSinistro({ ...sinistro });
    setIsEditing(false);
    setShowModal(true);
  };

  const iniciarEdicao = () => {
    setIsEditing(true);
  };

  const cancelarEdicao = () => {
    setEditedSinistro({ ...selectedSinistro });
    setIsEditing(false);
  };

  const handleEditChange = (campo, valor) => {
    setEditedSinistro(prev => ({
      ...prev,
      [campo]: valor
    }));
  };

  const salvarEdicao = async () => {
    try {
      // 👉  produção:
      // const res = await fetch(`/api/sinistros/${editedSinistro.id}`, {
      //   method: 'PUT',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(editedSinistro)
      // });
      // if (!res.ok) throw new Error('Erro ao salvar');

      // 👉  mock: atualiza o estado local
      setSinistros(prev => 
        prev.map(s => s.id === editedSinistro.id ? editedSinistro : s)
      );
      
      setSelectedSinistro(editedSinistro);
      setIsEditing(false);
      
      // Simula delay da API
      await new Promise(resolve => setTimeout(resolve, 500));
      
      alert('Sinistro atualizado com sucesso!');
    } catch (err) {
      console.error('Erro ao salvar sinistro:', err);
      alert('Erro ao salvar as alterações. Tente novamente.');
    }
  };

  const fecharModal = () => {
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
          </div>

          <div className="flex gap-3">
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
              sinistros.reduce(
                (total, s) => total + (s.valor_mercadoria ?? 0),
                0
              )
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
              <RefreshCw
                className="animate-spin mr-2"
                size={24}
              />
              <span>Carregando sinistros...</span>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <Th>Conhecimento</Th>
                    <Th>Cliente</Th>
                    <Th>Data</Th>
                    <Th>Modal</Th>
                    <Th>Ocorrência</Th>
                    <Th>Valor</Th>
                    <Th>Status</Th>
                    <Th>Ações</Th>
                  </tr>
                </thead>

                <tbody className="bg-white divide-y divide-gray-200">
                  {sinistros.map((s) => (
                    <tr
                      key={s.id}
                      className="hover:bg-gray-50"
                    >
                      <Td bold>{s.nr_conhecimento}</Td>
                      <Td>{s.cliente}</Td>
                      <Td>{formatarData(s.data_evento)}</Td>
                      <Td>{s.modal}</Td>
                      <Td>{s.tipo_ocorrencia}</Td>
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
              onChange={(value) => handleEditChange('nr_conhecimento', value)}
            />

            {/* Cliente */}
            <EditableField
              label="Cliente"
              value={editedSinistro.cliente}
              isEditing={isEditing}
              onChange={(value) => handleEditChange('cliente', value)}
            />
frontend/src/pages/Dashboard.jsx
            {/* Data do Evento */}
            <EditableField
              label="Data do Evento"
              value={isEditing ? formatarDataParaInput(editedSinistro.data_evento) : formatarData(editedSinistro.data_evento)}
              isEditing={isEditing}
              type={isEditing ? 'date' : 'text'}
              onChange={(value) => handleEditChange('data_evento', value)}
            />

            {/* Modal */}
            <EditableField
              label="Modal"
              value={editedSinistro.modal}
              isEditing={isEditing}
              type="select"
              options={[
                { value: 'Rodoviário', label: 'Rodoviário' },
                { value: 'Aéreo', label: 'Aéreo' }
              ]}
              onChange={(value) => handleEditChange('modal', value)}
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
                { value: 'Atraso', label: 'Atraso' }
              ]}
              onChange={(value) => handleEditChange('tipo_ocorrencia', value)}
            />

            {/* Valor da Mercadoria */}
            <EditableField
              label="Valor da Mercadoria"
              value={isEditing ? editedSinistro.valor_mercadoria : formatarMoeda(editedSinistro.valor_mercadoria)}
              isEditing={isEditing}
              type={isEditing ? 'number' : 'text'}
              step={isEditing ? '0.01' : undefined}
              onChange={(value) => handleEditChange('valor_mercadoria', parseFloat(value) || 0)}
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
                  className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${getStatusColor(editedSinistro.status)}`}
                >
                  {editedSinistro.status}
                </span>
              )}
            </div>

            {/* Botões de ação no modo de edição */}
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
  step
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
          {options.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
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
      <p className="text-sm text-gray-900 bg-gray-50 p-3 rounded-lg">
        {value}
      </p>
    )}
  </div>
);

export default SinistrosPage;