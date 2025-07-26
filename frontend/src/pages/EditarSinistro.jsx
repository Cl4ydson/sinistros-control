import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Save, 
  ArrowLeft, 
  Calculator,
  DollarSign,
  Calendar,
  User,
  Building,
  AlertTriangle,
  CheckCircle,
  Clock,
  Scale,
  Truck,
  MapPin,
  Phone,
  Mail,
  Hash,
  Percent,
  Plus,
  X,
  Shield
} from 'lucide-react';
import UltraProfessionalLayout from '../components/Layout/UltraProfessionalLayout';
import { useTheme } from '../contexts/ThemeContext';
import { useParams, useNavigate } from 'react-router-dom';
import SinistrosAPI from '../services/api';

const EditarSinistro = () => {
  const { isDark } = useTheme();
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(false);
  const [sinistro, setSinistro] = useState({
    // Dados básicos
    numero: 'SIN-2024-0001',
    nota: '',
    remetente: '',
    
    // Dados do sinistro
    observacoes: '',
    valorSinistro: 0,
    
    // Pagamento
    numeroND: '',
    dataVencimentoND: '',
    statusPagamento: 'Aguardando ND',
    
    // Indenizações
    responsavelAvaria: '',
    indenizado: false,
    statusIndenizacao: 'Pendente',
    programacaoPagamento: [{ data: '', valor: '', doctoESL: '' }],
    
    // Salvados
    valorVendido: 0,
    responsavelCompra: '',
    programacaoPagamentoSalvados: '',
    valorVenda: 0,
    percentualDesconto: 0,
    
    // Uso interno
    dataLiberacao: '',
    responsavelLiberacao: '',
    valorLiberado: 0,
    setorRecebimento: '',
    
    // Acionamento jurídico
    acionamentoJuridico: false,
    dataAberturaJuridico: '',
    custasJuridicas: 0,
    statusJuridico: 'Aguardando abertura',
    
    // Acionamento seguradora
    acionamentoSeguradora: false,
    dataAberturaSeguradora: '',
    seguradora: '',
    statusSeguradora: 'Aguardando abertura',
    programacaoIndenizacaoSeguradora: '',
    
    // Status geral
    status: 'Não iniciado'
  });

  const breadcrumbs = ['Sistema', 'Gestão', 'Sinistros', 'Editar'];

  const headerActions = [
    { icon: Save, variant: 'primary', onClick: handleSave },
    { icon: ArrowLeft, onClick: () => navigate('/sinistros') }
  ];

  const responsaveisAvaria = [
    'Transportadora',
    'Cliente - Remetente',
    'Cliente - Destinatário',
    'Terceiros',
    'Seguradora',
    'Causa Externa',
    'A definir'
  ];

  const seguradoras = [
    'Porto Seguro',
    'Bradesco Seguros',
    'Allianz',
    'Zurich',
    'Mapfre',
    'SulAmérica',
    'Liberty',
    'Tokio Marine'
  ];

  const setores = [
    'Operações',
    'Comercial',
    'Administrativo',
    'Recursos Humanos',
    'TI',
    'Qualidade',
    'Segurança',
    'Manutenção'
  ];

  useEffect(() => {
    if (id) {
      loadSinistro(id);
    }
  }, [id]);

  const loadSinistro = async (sinistroId) => {
    setLoading(true);
    try {
      // Primeiro tentar carregar da API de automação
      let result;
      try {
        // Tentar buscar por ID primeiro
        result = await SinistrosAPI.obterSinistroAutomacao(sinistroId);
      } catch (error) {
        // Se der 404, tentar buscar pela nota fiscal na API de automação
        try {
          result = await SinistrosAPI.obterSinistroAutomacaoPorNota(sinistroId);
        } catch {
          result = { success: false };
        }
      }
      
      if (result.success && result.data) {
        // Mapear dados da API de automação para o formato do frontend
        const dadosAPI = result.data;
        setSinistro({
          ...sinistro,
          numero: dadosAPI.id || sinistroId,
          nota: dadosAPI.nota_fiscal || '',
          status: dadosAPI.status_geral || 'Não iniciado',
          
          // Dados de pagamento
          statusPagamento: dadosAPI.status_pagamento || 'Aguardando ND',
          numeroND: dadosAPI.numero_nd || '',
          dataVencimentoND: dadosAPI.data_vencimento_nd || '',
          
          // Dados de indenização
          statusIndenizacao: dadosAPI.status_indenizacao || 'Pendente',
          valorSinistro: dadosAPI.valor_indenizacao || 0,
          responsavelAvaria: dadosAPI.responsavel_avaria || '',
          indenizado: dadosAPI.indenizado || false,
          
          // Salvados
          valorVendido: dadosAPI.valor_salvados_vendido || 0,
          responsavelCompra: dadosAPI.responsavel_compra_salvados || '',
          valorVenda: dadosAPI.valor_venda_salvados || 0,
          percentualDesconto: dadosAPI.percentual_desconto_salvados || 0,
          
          // Uso interno
          setorRecebimento: dadosAPI.setor_responsavel || '',
          responsavelLiberacao: dadosAPI.responsavel_interno || '',
          dataLiberacao: dadosAPI.data_liberacao || '',
          valorLiberado: dadosAPI.valor_liberado || 0,
          
          // Jurídico
          acionamentoJuridico: dadosAPI.acionamento_juridico || false,
          statusJuridico: dadosAPI.status_juridico || 'Não acionado',
          dataAberturaJuridico: dadosAPI.data_abertura_juridico || '',
          custasJuridicas: dadosAPI.custas_juridicas || 0,
          
          // Seguradora
          acionamentoSeguradora: dadosAPI.acionamento_seguradora || false,
          statusSeguradora: dadosAPI.status_seguradora || 'Não acionado',
          seguradora: dadosAPI.nome_seguradora || '',
          dataAberturaSeguradora: dadosAPI.data_abertura_seguradora || '',
          programacaoIndenizacaoSeguradora: dadosAPI.programacao_indenizacao_seguradora || '',
          
          observacoes: dadosAPI.observacoes_pagamento || dadosAPI.observacoes_internas || '',
          
          // Carregar programação de pagamento se existir
          programacaoPagamento: dadosAPI.programacao_pagamento || [{ data: '', valor: '', doctoESL: '' }]
        });
      }
    } catch (error) {
      console.error('Erro ao carregar sinistro da automação:', error);
      
      // Se falhar na automação, tentar carregar da API de consulta como fallback
      try {
        const result = await SinistrosAPI.obterSinistro(sinistroId);
        if (result.success && result.data) {
          const dadosAPI = result.data;
          setSinistro({
            ...sinistro,
            numero: dadosAPI.numero || sinistroId,
            nota: dadosAPI.nota_fiscal || dadosAPI.numero_documento || '',
            status: 'Não iniciado', // Novo sinistro que será criado na automação
            valorSinistro: dadosAPI.valor_sinistro || 0,
            observacoes: dadosAPI.observacoes || ''
          });
        }
      } catch (fallbackError) {
        console.error('Erro ao carregar de ambas as APIs:', fallbackError);
        alert(`❌ Erro ao carregar sinistro: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  async function handleSave() {
    setLoading(true);
    try {
      // Mapear dados do frontend para o formato da API de automação
      const dadosParaAPI = {
        // Dados básicos
        nota_fiscal: sinistro.nota,
        status_geral: sinistro.status,
        
        // Dados de pagamento
        status_pagamento: sinistro.statusPagamento,
        numero_nd: sinistro.numeroND,
        data_vencimento_nd: sinistro.dataVencimentoND,
        observacoes_pagamento: sinistro.observacoes,
        
        // Dados de indenização
        status_indenizacao: sinistro.statusIndenizacao,
        valor_indenizacao: sinistro.valorSinistro,
        responsavel_avaria: sinistro.responsavelAvaria,
        indenizado: sinistro.indenizado,
        
        // Salvados
        valor_salvados_vendido: sinistro.valorVendido,
        responsavel_compra_salvados: sinistro.responsavelCompra,
        valor_venda_salvados: sinistro.valorVenda,
        percentual_desconto_salvados: sinistro.percentualDesconto,
        
        // Uso interno
        setor_responsavel: sinistro.setorRecebimento,
        responsavel_interno: sinistro.responsavelLiberacao,
        data_liberacao: sinistro.dataLiberacao,
        valor_liberado: sinistro.valorLiberado,
        observacoes_internas: sinistro.observacoes,
        
        // Jurídico
        acionamento_juridico: sinistro.acionamentoJuridico,
        status_juridico: sinistro.statusJuridico,
        data_abertura_juridico: sinistro.dataAberturaJuridico,
        custas_juridicas: sinistro.custasJuridicas,
        
        // Seguradora
        acionamento_seguradora: sinistro.acionamentoSeguradora,
        status_seguradora: sinistro.statusSeguradora,
        nome_seguradora: sinistro.seguradora,
        data_abertura_seguradora: sinistro.dataAberturaSeguradora,
        programacao_indenizacao_seguradora: sinistro.programacaoIndenizacaoSeguradora,
        
        // Programação de pagamento
        programacao_pagamento: sinistro.programacaoPagamento
      };

      // Chamar API de automação para salvar na tabela Sinistros (criar ou atualizar)
      const response = await fetch(`http://127.0.0.1:8001/api/automacao/sinistros/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dadosParaAPI)
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success) {
        alert('✅ Sinistro salvo com sucesso na tabela Sinistros!');
        
        // Fechar tela e voltar para lista de sinistros
        setTimeout(() => {
          navigate('/sinistros');
        }, 1000);
      } else {
        throw new Error(result.message || 'Erro ao salvar');
      }
    } catch (error) {
      console.error('Erro ao salvar sinistro:', error);
      alert(`❌ Erro ao salvar na tabela Sinistros: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  const updateSinistro = (field, value) => {
    setSinistro(prev => ({ ...prev, [field]: value }));
  };

  const addProgramacaoPagamento = () => {
    if (sinistro.programacaoPagamento.length < 10) {
      setSinistro(prev => ({
        ...prev,
        programacaoPagamento: [...prev.programacaoPagamento, { data: '', valor: '', doctoESL: '' }]
      }));
    }
  };

  const removeProgramacaoPagamento = (index) => {
    setSinistro(prev => ({
      ...prev,
      programacaoPagamento: prev.programacaoPagamento.filter((_, i) => i !== index)
    }));
  };

  const updateProgramacaoPagamento = (index, field, value) => {
    setSinistro(prev => ({
      ...prev,
      programacaoPagamento: prev.programacaoPagamento.map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const calcularPrejuizo = () => {
    const valorSinistro = sinistro.valorSinistro || 0;
    const valorIndenizado = sinistro.programacaoPagamento.reduce((sum, p) => sum + (parseFloat(p.valor) || 0), 0);
    const valorUsoInterno = sinistro.valorLiberado || 0;
    const valorSeguradoras = 0;
    const valorJuridico = sinistro.custasJuridicas || 0;
    const valorSalvados = sinistro.valorVendido || 0;
    
    return valorSinistro - valorIndenizado - valorUsoInterno - valorSeguradoras - valorJuridico - valorSalvados;
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value || 0);
  };

  return (
    <UltraProfessionalLayout 
      title={`Editar Sinistro (${sinistro.nota || sinistro.numero})`}
      subtitle="Gestão completa de tratativas e controles"
      breadcrumbs={breadcrumbs}
      headerActions={headerActions}
    >
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500" />
        </div>
      ) : (
        <div className="space-y-8">
          {/* Campo de Busca */}
          <div className={`
            p-4 rounded-xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3">
              <input
                type="text"
                placeholder="Buscar em todos os campos do sinistro..."
                className={`
                  flex-1 p-3 rounded-lg border transition-colors
                  ${isDark
                    ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                    : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                  }
                  focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                `}
                onChange={(e) => {
                  // Implementar busca em tempo real nos campos
                  const termo = e.target.value.toLowerCase();
                  // Por enquanto apenas visual - funcionalidade pode ser expandida
                  console.log('Buscando por:', termo);
                }}
              />
            </div>
          </div>

          {/* Dados Básicos */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Dados Básicos
              </h2>
            </div>
            
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Número da Nota
                </label>
                <input
                  type="text"
                  value={sinistro.nota}
                  onChange={(e) => updateSinistro('nota', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark
                      ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                  placeholder="Ex: 123456"
                />
              </div>

              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Status Geral
                </label>
                <select
                  value={sinistro.status}
                  onChange={(e) => updateSinistro('status', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                >
                  <option value="Não iniciado">Não iniciado</option>
                  <option value="Em andamento">Em andamento</option>
                  <option value="Concluído">Concluído</option>
                  <option value="Não sinistrado">Não sinistrado</option>
                </select>
              </div>
            </div>
          </div>

          {/* Dados do Sinistro */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-red-500 to-pink-500 rounded-xl flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Dados do Sinistro
              </h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Observações
                </label>
                <textarea
                  value={sinistro.observacoes}
                  onChange={(e) => updateSinistro('observacoes', e.target.value)}
                  rows={4}
                  className={`
                    w-full p-3 rounded-xl border transition-colors resize-none
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                  placeholder="Descreva os detalhes do sinistro..."
                />
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Valor do Sinistro
                </label>
                <div className="relative">
                  <DollarSign className={`absolute left-3 top-3 w-5 h-5 ${isDark ? 'text-slate-400' : 'text-gray-500'}`} />
                  <input
                    type="number"
                    step="0.01"
                    value={sinistro.valorSinistro}
                    onChange={(e) => updateSinistro('valorSinistro', parseFloat(e.target.value) || 0)}
                    className={`
                      w-full pl-11 pr-4 py-3 rounded-xl border transition-colors
                      ${isDark 
                        ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                        : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                      }
                      focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    `}
                    placeholder="0,00"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Pagamento */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
                <DollarSign className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Pagamento
              </h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Nº ND
                </label>
                <input
                  type="text"
                  value={sinistro.numeroND}
                  onChange={(e) => updateSinistro('numeroND', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                  placeholder="Número da ND"
                />
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Data Vencimento ND
                </label>
                <input
                  type="date"
                  value={sinistro.dataVencimentoND}
                  onChange={(e) => updateSinistro('dataVencimentoND', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                />
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Status de Pagamento
                </label>
                <select
                  value={sinistro.statusPagamento}
                  onChange={(e) => updateSinistro('statusPagamento', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                >
                  <option value="Aguardando ND">Aguardando ND</option>
                  <option value="Aguardando Pagamento">Aguardando Pagamento</option>
                  <option value="Pago">Pago</option>
                  <option value="Em tratativa">Em tratativa</option>
                </select>
              </div>
            </div>
          </div>

          {/* Indenizações */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-xl flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Indenizações
              </h2>
            </div>
            
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                    Responsável pela Avaria
                  </label>
                  <select
                    value={sinistro.responsavelAvaria}
                    onChange={(e) => updateSinistro('responsavelAvaria', e.target.value)}
                    className={`
                      w-full p-3 rounded-xl border transition-colors
                      ${isDark 
                        ? 'bg-slate-900/60 border-slate-700 text-white' 
                        : 'bg-gray-50/60 border-gray-300 text-gray-900'
                      }
                      focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    `}
                  >
                    <option value="">Selecione...</option>
                    {responsaveisAvaria.map((resp) => (
                      <option key={resp} value={resp}>{resp}</option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                    Indenizado?
                  </label>
                  <select
                    value={sinistro.indenizado ? 'Sim' : 'Não'}
                    onChange={(e) => updateSinistro('indenizado', e.target.value === 'Sim')}
                    className={`
                      w-full p-3 rounded-xl border transition-colors
                      ${isDark 
                        ? 'bg-slate-900/60 border-slate-700 text-white' 
                        : 'bg-gray-50/60 border-gray-300 text-gray-900'
                      }
                      focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    `}
                  >
                    <option value="Não">Não</option>
                    <option value="Sim">Sim</option>
                  </select>
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                    Status Indenização
                  </label>
                  <select
                    value={sinistro.statusIndenizacao}
                    onChange={(e) => updateSinistro('statusIndenizacao', e.target.value)}
                    className={`
                      w-full p-3 rounded-xl border transition-colors
                      ${isDark 
                        ? 'bg-slate-900/60 border-slate-700 text-white' 
                        : 'bg-gray-50/60 border-gray-300 text-gray-900'
                      }
                      focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    `}
                  >
                    <option value="Programado">Programado</option>
                    <option value="Pago">Pago</option>
                    <option value="Pendente">Pendente</option>
                    <option value="Pago Parcial">Pago Parcial</option>
                  </select>
                </div>
              </div>
              
              {sinistro.indenizado && (
                <div className={`
                  p-4 rounded-xl border
                  ${isDark ? 'bg-slate-900/40 border-slate-600' : 'bg-gray-50/40 border-gray-300'}
                `}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className={`font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                      Programação de Pagamento
                    </h3>
                    <button
                      onClick={addProgramacaoPagamento}
                      disabled={sinistro.programacaoPagamento.length >= 10}
                      className={`
                        px-3 py-1 rounded-lg text-sm font-medium transition-colors
                        ${sinistro.programacaoPagamento.length >= 10
                          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                          : 'bg-blue-500 text-white hover:bg-blue-600'
                        }
                      `}
                    >
                      <Plus className="w-4 h-4 mr-1 inline" />
                      Adicionar Data
                    </button>
                  </div>
                  
                  <div className="space-y-3">
                    {sinistro.programacaoPagamento.map((prog, index) => (
                      <div key={index} className="grid grid-cols-1 md:grid-cols-4 gap-3 items-end">
                        <div>
                          <label className={`block text-xs font-medium mb-1 ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                            Data
                          </label>
                          <input
                            type="date"
                            value={prog.data}
                            onChange={(e) => updateProgramacaoPagamento(index, 'data', e.target.value)}
                            className={`
                              w-full p-2 rounded-lg border text-sm
                              ${isDark 
                                ? 'bg-slate-800 border-slate-600 text-white' 
                                : 'bg-white border-gray-300 text-gray-900'
                              }
                            `}
                          />
                        </div>
                        <div>
                          <label className={`block text-xs font-medium mb-1 ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                            Valor
                          </label>
                          <input
                            type="number"
                            step="0.01"
                            value={prog.valor}
                            onChange={(e) => updateProgramacaoPagamento(index, 'valor', e.target.value)}
                            className={`
                              w-full p-2 rounded-lg border text-sm
                              ${isDark 
                                ? 'bg-slate-800 border-slate-600 text-white' 
                                : 'bg-white border-gray-300 text-gray-900'
                              }
                            `}
                            placeholder="0,00"
                          />
                        </div>
                        <div>
                          <label className={`block text-xs font-medium mb-1 ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                            Docto ESL
                          </label>
                          <input
                            type="text"
                            value={prog.doctoESL}
                            onChange={(e) => updateProgramacaoPagamento(index, 'doctoESL', e.target.value)}
                            className={`
                              w-full p-2 rounded-lg border text-sm
                              ${isDark 
                                ? 'bg-slate-800 border-slate-600 text-white' 
                                : 'bg-white border-gray-300 text-gray-900'
                              }
                            `}
                            placeholder="Boleto/Título"
                          />
                        </div>
                        <button
                          onClick={() => removeProgramacaoPagamento(index)}
                          className="p-2 text-red-500 hover:bg-red-100 rounded-lg transition-colors"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Salvados */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
                <Truck className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Salvados
              </h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Valor Vendido
                </label>
                <div className="relative">
                  <DollarSign className={`absolute left-3 top-3 w-5 h-5 ${isDark ? 'text-slate-400' : 'text-gray-500'}`} />
                  <input
                    type="number"
                    step="0.01"
                    value={sinistro.valorVendido}
                    onChange={(e) => updateSinistro('valorVendido', parseFloat(e.target.value) || 0)}
                    className={`
                      w-full pl-11 pr-4 py-3 rounded-xl border transition-colors
                      ${isDark 
                        ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                        : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                      }
                      focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    `}
                    placeholder="0,00"
                  />
                </div>
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Responsável pela Compra
                </label>
                <input
                  type="text"
                  value={sinistro.responsavelCompra}
                  onChange={(e) => updateSinistro('responsavelCompra', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                  placeholder="Nome do responsável"
                />
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Valor da Venda
                </label>
                <div className="relative">
                  <DollarSign className={`absolute left-3 top-3 w-5 h-5 ${isDark ? 'text-slate-400' : 'text-gray-500'}`} />
                  <input
                    type="number"
                    step="0.01"
                    value={sinistro.valorVenda}
                    onChange={(e) => updateSinistro('valorVenda', parseFloat(e.target.value) || 0)}
                    className={`
                      w-full pl-11 pr-4 py-3 rounded-xl border transition-colors
                      ${isDark 
                        ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                        : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                      }
                      focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    `}
                    placeholder="0,00"
                  />
                </div>
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  % de Desconto
                </label>
                <div className="relative">
                  <Percent className={`absolute left-3 top-3 w-5 h-5 ${isDark ? 'text-slate-400' : 'text-gray-500'}`} />
                  <input
                    type="number"
                    step="0.01"
                    max="100"
                    value={sinistro.percentualDesconto}
                    onChange={(e) => updateSinistro('percentualDesconto', parseFloat(e.target.value) || 0)}
                    className={`
                      w-full pl-11 pr-4 py-3 rounded-xl border transition-colors
                      ${isDark 
                        ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                        : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                      }
                      focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    `}
                    placeholder="0,00"
                  />
                </div>
              </div>
              
              <div className="md:col-span-2">
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Programação de Pagamento
                </label>
                <input
                  type="text"
                  value={sinistro.programacaoPagamentoSalvados}
                  onChange={(e) => updateSinistro('programacaoPagamentoSalvados', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                  placeholder="Detalhes da programação"
                />
              </div>
            </div>
          </div>

          {/* Uso Interno */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-xl flex items-center justify-center">
                <Building className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Uso Interno
              </h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Data da Liberação
                </label>
                <input
                  type="date"
                  value={sinistro.dataLiberacao}
                  onChange={(e) => updateSinistro('dataLiberacao', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                />
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Responsável pela Liberação
                </label>
                <input
                  type="text"
                  value={sinistro.responsavelLiberacao}
                  onChange={(e) => updateSinistro('responsavelLiberacao', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                  placeholder="Nome do responsável"
                />
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Valor Liberado
                </label>
                <div className="relative">
                  <DollarSign className={`absolute left-3 top-3 w-5 h-5 ${isDark ? 'text-slate-400' : 'text-gray-500'}`} />
                  <input
                    type="number"
                    step="0.01"
                    value={sinistro.valorLiberado}
                    onChange={(e) => updateSinistro('valorLiberado', parseFloat(e.target.value) || 0)}
                    className={`
                      w-full pl-11 pr-4 py-3 rounded-xl border transition-colors
                      ${isDark 
                        ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                        : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                      }
                      focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                    `}
                    placeholder="0,00"
                  />
                </div>
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Setor Recebimento
                </label>
                <select
                  value={sinistro.setorRecebimento}
                  onChange={(e) => updateSinistro('setorRecebimento', e.target.value)}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                >
                  <option value="">Selecione o setor...</option>
                  {setores.map((setor) => (
                    <option key={setor} value={setor}>{setor}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Acionamento Jurídico */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl flex items-center justify-center">
                <Scale className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Acionamento Jurídico
              </h2>
            </div>
            
            <div className="space-y-6">
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Acionamento Jurídico?
                </label>
                <select
                  value={sinistro.acionamentoJuridico ? 'Sim' : 'Não'}
                  onChange={(e) => updateSinistro('acionamentoJuridico', e.target.value === 'Sim')}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                >
                  <option value="Não">Não</option>
                  <option value="Sim">Sim</option>
                </select>
              </div>
              
              {sinistro.acionamentoJuridico && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                      Data Abertura
                    </label>
                    <input
                      type="date"
                      value={sinistro.dataAberturaJuridico}
                      onChange={(e) => updateSinistro('dataAberturaJuridico', e.target.value)}
                      className={`
                        w-full p-3 rounded-xl border transition-colors
                        ${isDark 
                          ? 'bg-slate-900/60 border-slate-700 text-white' 
                          : 'bg-gray-50/60 border-gray-300 text-gray-900'
                        }
                        focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                      `}
                    />
                  </div>
                  
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                      Custas Jurídicas
                    </label>
                    <div className="relative">
                      <DollarSign className={`absolute left-3 top-3 w-5 h-5 ${isDark ? 'text-slate-400' : 'text-gray-500'}`} />
                      <input
                        type="number"
                        step="0.01"
                        value={sinistro.custasJuridicas}
                        onChange={(e) => updateSinistro('custasJuridicas', parseFloat(e.target.value) || 0)}
                        className={`
                          w-full pl-11 pr-4 py-3 rounded-xl border transition-colors
                          ${isDark 
                            ? 'bg-slate-900/60 border-slate-700 text-white placeholder-slate-400' 
                            : 'bg-gray-50/60 border-gray-300 text-gray-900 placeholder-gray-500'
                          }
                          focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                        `}
                        placeholder="0,00"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                      Status Jurídico
                    </label>
                    <select
                      value={sinistro.statusJuridico}
                      onChange={(e) => updateSinistro('statusJuridico', e.target.value)}
                      className={`
                        w-full p-3 rounded-xl border transition-colors
                        ${isDark 
                          ? 'bg-slate-900/60 border-slate-700 text-white' 
                          : 'bg-gray-50/60 border-gray-300 text-gray-900'
                        }
                        focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                      `}
                    >
                      <option value="Aguardando abertura">Aguardando abertura</option>
                      <option value="Processo iniciado">Processo iniciado</option>
                      <option value="Indenizado">Indenizado</option>
                    </select>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Acionamento Seguradora */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Acionamento Seguradora
              </h2>
            </div>
            
            <div className="space-y-6">
              <div>
                <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                  Acionamento Seguradora?
                </label>
                <select
                  value={sinistro.acionamentoSeguradora ? 'Sim' : 'Não'}
                  onChange={(e) => updateSinistro('acionamentoSeguradora', e.target.value === 'Sim')}
                  className={`
                    w-full p-3 rounded-xl border transition-colors
                    ${isDark 
                      ? 'bg-slate-900/60 border-slate-700 text-white' 
                      : 'bg-gray-50/60 border-gray-300 text-gray-900'
                    }
                    focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                  `}
                >
                  <option value="Não">Não</option>
                  <option value="Sim">Sim</option>
                </select>
              </div>
              
              {sinistro.acionamentoSeguradora && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                      Data Abertura
                    </label>
                    <input
                      type="date"
                      value={sinistro.dataAberturaSeguradora}
                      onChange={(e) => updateSinistro('dataAberturaSeguradora', e.target.value)}
                      className={`
                        w-full p-3 rounded-xl border transition-colors
                        ${isDark 
                          ? 'bg-slate-900/60 border-slate-700 text-white' 
                          : 'bg-gray-50/60 border-gray-300 text-gray-900'
                        }
                        focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                      `}
                    />
                  </div>
                  
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                      Seguradora
                    </label>
                    <select
                      value={sinistro.seguradora}
                      onChange={(e) => updateSinistro('seguradora', e.target.value)}
                      className={`
                        w-full p-3 rounded-xl border transition-colors
                        ${isDark 
                          ? 'bg-slate-900/60 border-slate-700 text-white' 
                          : 'bg-gray-50/60 border-gray-300 text-gray-900'
                        }
                        focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                      `}
                    >
                      <option value="">Selecione...</option>
                      {seguradoras.map((seg) => (
                        <option key={seg} value={seg}>{seg}</option>
                      ))}
                    </select>
                  </div>
                  
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                      Status Seguradora
                    </label>
                    <select
                      value={sinistro.statusSeguradora}
                      onChange={(e) => updateSinistro('statusSeguradora', e.target.value)}
                      className={`
                        w-full p-3 rounded-xl border transition-colors
                        ${isDark 
                          ? 'bg-slate-900/60 border-slate-700 text-white' 
                          : 'bg-gray-50/60 border-gray-300 text-gray-900'
                        }
                        focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                      `}
                    >
                      <option value="Aguardando abertura">Aguardando abertura</option>
                      <option value="Processo iniciado">Processo iniciado</option>
                      <option value="Indenizado">Indenizado</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className={`block text-sm font-medium mb-2 ${isDark ? 'text-slate-300' : 'text-gray-700'}`}>
                      Programação Indenização
                    </label>
                    <input
                      type="date"
                      value={sinistro.programacaoIndenizacaoSeguradora}
                      onChange={(e) => updateSinistro('programacaoIndenizacaoSeguradora', e.target.value)}
                      className={`
                        w-full p-3 rounded-xl border transition-colors
                        ${isDark 
                          ? 'bg-slate-900/60 border-slate-700 text-white' 
                          : 'bg-gray-50/60 border-gray-300 text-gray-900'
                        }
                        focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500
                      `}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Cálculo do Prejuízo */}
          <div className={`
            p-6 rounded-2xl border backdrop-blur-sm
            ${isDark ? 'bg-gradient-to-r from-red-900/40 to-pink-900/40 border-red-700/50' : 'bg-gradient-to-r from-red-50/40 to-pink-50/40 border-red-200/50'}
          `}>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-red-500 to-pink-500 rounded-xl flex items-center justify-center">
                <Calculator className="w-5 h-5 text-white" />
              </div>
              <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Cálculo do Prejuízo Final
              </h2>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
              <div className="text-center">
                <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                  Valor Sinistro
                </p>
                <p className={`text-lg font-bold ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  {formatCurrency(sinistro.valorSinistro)}
                </p>
              </div>
              <div className="text-center">
                <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                  Indenizações
                </p>
                <p className={`text-lg font-bold text-red-500`}>
                  -{formatCurrency(sinistro.programacaoPagamento.reduce((sum, p) => sum + (parseFloat(p.valor) || 0), 0))}
                </p>
              </div>
              <div className="text-center">
                <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                  Uso Interno
                </p>
                <p className={`text-lg font-bold text-green-500`}>
                  -{formatCurrency(sinistro.valorLiberado)}
                </p>
              </div>
              <div className="text-center">
                <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                  Seguradora
                </p>
                <p className={`text-lg font-bold text-blue-500`}>
                  -{formatCurrency(0)}
                </p>
              </div>
              <div className="text-center">
                <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                  Jurídico
                </p>
                <p className={`text-lg font-bold text-purple-500`}>
                  -{formatCurrency(sinistro.custasJuridicas)}
                </p>
              </div>
              <div className="text-center">
                <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-gray-600'}`}>
                  Salvados
                </p>
                <p className={`text-lg font-bold text-orange-500`}>
                  -{formatCurrency(sinistro.valorVendido)}
                </p>
              </div>
            </div>
            
            <div className={`
              p-4 rounded-xl text-center border-2 border-dashed
              ${calcularPrejuizo() > 0 
                ? 'border-red-400 bg-red-50/50' 
                : 'border-green-400 bg-green-50/50'
              }
            `}>
              <p className={`text-sm font-medium ${isDark ? 'text-slate-400' : 'text-gray-600'} mb-2`}>
                PREJUÍZO FINAL
              </p>
              <p className={`text-3xl font-bold ${calcularPrejuizo() > 0 ? 'text-red-600' : 'text-green-600'}`}>
                {formatCurrency(calcularPrejuizo())}
              </p>
            </div>
          </div>
        </div>
      )}
        {/* Botão de Salvar no Final */}
        <div className={`
          mt-8 p-6 rounded-2xl border backdrop-blur-sm
          ${isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white/60 border-gray-200'}
        `}>
          <div className="flex justify-center">
            <button
              onClick={handleSave}
              disabled={loading}
              className={`
                px-8 py-4 rounded-xl font-medium text-lg transition-all duration-200
                flex items-center space-x-3
                ${loading 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 transform hover:scale-105'
                }
                text-white shadow-lg
              `}
            >
              <Save className="w-6 h-6" />
              <span>{loading ? 'Salvando...' : 'Salvar Alterações'}</span>
            </button>
          </div>
        </div>

    </UltraProfessionalLayout>
  );
};

export default EditarSinistro; 