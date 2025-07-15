import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import Login from './pages/Login';
import Register from './pages/Register';
import DashboardUltraProfessional from './pages/DashboardUltraProfessional';
import SinistrosUltraProfessional from './pages/SinistrosUltraProfessional';
import RelatoriosUltraProfessional from './pages/RelatoriosUltraProfessional';
import SinistrosSimple from './pages/SinistrosSimple';
import EditarSinistro from './pages/EditarSinistro';
import TestePage from './pages/TestePage';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<DashboardUltraProfessional />} />
            <Route path="/sinistros" element={<SinistrosUltraProfessional />} />
            <Route path="/relatorios" element={<RelatoriosUltraProfessional />} />
            <Route path="/sinistros/editar/:id" element={<EditarSinistro />} />
            <Route path="/teste" element={<TestePage />} />
            {/* Rotas do novo sistema ultra profissional */}
            <Route path="/analytics" element={<DashboardUltraProfessional />} />
            <Route path="/historico" element={<DashboardUltraProfessional />} />
            <Route path="/alertas" element={<DashboardUltraProfessional />} />
            <Route path="/usuarios" element={<DashboardUltraProfessional />} />
            <Route path="/sistema" element={<DashboardUltraProfessional />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
