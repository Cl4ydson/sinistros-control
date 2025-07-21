// Mock data for demo mode when backend is not available

export const mockSinistros = [
  {
    id: 1,
    nota_fiscal: "000001234",
    conhecimento: "CTR-2024-001",
    remetente: "Empresa ABC Ltda",
    destinatario: "Distribuidora XYZ",
    dt_coleta: "2024-01-15",
    dt_evento: "2024-01-16",
    tipo_ocorrencia: "Avaria Parcial",
    descricao_ocorrencia: "Produto danificado durante transporte",
    status: "Em análise",
    valor_mercadoria: 15000.00,
    valor_prejuizo: 2500.00
  },
  {
    id: 2,
    nota_fiscal: "000001235",
    conhecimento: "CTR-2024-002",
    remetente: "Indústria DEF S.A.",
    destinatario: "Comércio GHI",
    dt_coleta: "2024-01-14",
    dt_evento: "2024-01-15",
    tipo_ocorrencia: "Roubo de Carga",
    descricao_ocorrencia: "Roubo total da mercadoria",
    status: "Concluído",
    valor_mercadoria: 50000.00,
    valor_prejuizo: 50000.00
  },
  {
    id: 3,
    nota_fiscal: "000001236",
    conhecimento: "CTR-2024-003",
    remetente: "Fornecedor JKL",
    destinatario: "Loja MNO",
    dt_coleta: "2024-01-13",
    dt_evento: "2024-01-14",
    tipo_ocorrencia: "Extravio Parcial",
    descricao_ocorrencia: "Perda de parte da mercadoria",
    status: "Em análise",
    valor_mercadoria: 8000.00,
    valor_prejuizo: 1200.00
  }
];

export const mockDashboardData = {
  total_sinistros: 1247,
  avarias: 543,
  extravios: 298,
  roubos: 156,
  sinistradas: 250,
  valor_total_prejuizo: 2450000.00,
  status_conexao: "Demo Mode - Dados simulados"
};

export const mockEstatisticas = {
  total: 1247,
  por_tipo: {
    "Avaria Parcial": 320,
    "Avaria Total": 223,
    "Extravio Parcial": 180,
    "Extravio Total": 118,
    "Roubo de Carga": 156,
    "Mercadoria Sinistrada": 250
  },
  por_mes: {
    "2024-01": 89,
    "2024-02": 103,
    "2024-03": 127,
    "2024-04": 95,
    "2024-05": 134,
    "2024-06": 145,
    "2024-07": 156,
    "2024-08": 139,
    "2024-09": 127,
    "2024-10": 132
  },
  valor_total: 2450000.00,
  valor_medio: 1965.00
};

export const mockRelatorioPrejuizo = {
  total_geral: 2450000.00,
  por_setor: [
    { setor: "Eletrônicos", valor: 890000.00, quantidade: 234 },
    { setor: "Alimentos", valor: 456000.00, quantidade: 189 },
    { setor: "Vestuário", valor: 345000.00, quantidade: 156 },
    { setor: "Farmacêutico", valor: 278000.00, quantidade: 89 },
    { setor: "Automotivo", valor: 234000.00, quantidade: 67 },
    { setor: "Outros", valor: 247000.00, quantidade: 134 }
  ],
  tendencia_mensal: [
    { mes: "Jan/2024", valor: 187000 },
    { mes: "Fev/2024", valor: 234000 },
    { mes: "Mar/2024", valor: 298000 },
    { mes: "Abr/2024", valor: 213000 },
    { mes: "Mai/2024", valor: 267000 },
    { mes: "Jun/2024", valor: 289000 },
    { mes: "Jul/2024", valor: 312000 },
    { mes: "Ago/2024", valor: 278000 },
    { mes: "Set/2024", valor: 245000 },
    { mes: "Out/2024", valor: 267000 }
  ]
};

// Utility function to simulate API delay
export const simulateApiDelay = (ms = 500) => {
  return new Promise(resolve => setTimeout(resolve, ms));
};