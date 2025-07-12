import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  DollarSign,
  Clock,
  Users,
  BarChart3,
  Plus,
  Eye,
  ArrowUpRight
} from 'lucide-react';
import MainLayout from '../components/Layout/MainLayout';
import StatsCard from '../components/UI/StatsCard';
import ActionButton from '../components/UI/ActionButton';
import AlertCard from '../components/UI/AlertCard';
import { useTheme } from '../contexts/ThemeContext';
import UltraProfessionalLayout from '../components/Layout/UltraProfessionalLayout';

const Dashboard = () => {
  const { isDark } = useTheme();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [alerts, setAlerts] = useState([
    {
      id: 1,
      type: 'warning',
      title: 'Estoque Baixo',
      description: '5 produtos com estoque crítico',
      actions: [
        { label: 'Ver Produtos', variant: 'primary', onClick: () => console.log('Ver produtos') }
      ]
    },
    {
      id: 2,
      type: 'success',
      title: 'Sistema Atualizado',
      description: 'Última atualização agora',
      onClose: () => setAlerts(prev => prev.filter(alert => alert.id !== 2))
    }
  ]);

  // Simular carregamento de dados
  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);
      // Simular API delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setDashboardData({
        totalSinistros: 42,
        sinistrosAbertos: 10,
        sinistrosConcluidos: 27,
        valorTotal: 1250000,
        tendencias: {
          sinistros: { trend: 'up', value: '+12%' },
          valores: { trend: 'down', value: '-5%' },
          conclusoes: { trend: 'up', value: '+8%' }
        },
        atividadesRecentes: [
          {
            id: 1,
            tipo: 'entrada',
            descricao: 'Entrada de 100 unidades',
            tempo: '15 min'
          },
          {
            id: 2,
            tipo: 'entrada',
            descricao: 'Entrada de 200 unidades',
            tempo: '1h'
          },
          {
            id: 3,
            tipo: 'saida',
            descricao: 'Saída de 50 unidades',
            tempo: '2h'
          }
        ]
      });
      setLoading(false);
    };

    loadDashboardData();
  }, []);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  return (
    <UltraProfessionalLayout
      title="Dashboard"
      subtitle="Bem-vindo ao Sistema de Gestão de Sinistros"
      breadcrumbs={['Início', 'Dashboard']}
    >
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">Sistema de Gestão de Sinistros</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">Total de Sinistros</h3>
            <p className="text-3xl font-bold text-blue-600">150</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">Em Análise</h3>
            <p className="text-3xl font-bold text-yellow-600">45</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">Aprovados</h3>
            <p className="text-3xl font-bold text-green-600">85</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">Rejeitados</h3>
            <p className="text-3xl font-bold text-red-600">20</p>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Últimos Sinistros</h2>
          <p className="text-gray-600">Lista de sinistros recentes será exibida aqui...</p>
        </div>
      </div>
    </UltraProfessionalLayout>
  );
};

export default Dashboard;