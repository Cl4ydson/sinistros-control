import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../utils/api";

export default function Login() {
  const [login, setLogin] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const testConnection = async () => {
    setLoading(true);
    setErro(null);
    
    try {
      console.log("🔧 Testando conexão com banco...");
      const { data } = await api.get("/auth/test-db");
      console.log("✅ Teste de conexão:", data);
      setErro(`✅ ${data.message}`);
    } catch (err) {
      console.error("❌ Erro no teste:", err);
      if (err.response?.data?.detail) {
        setErro(`❌ Teste falhou: ${err.response.data.detail}`);
      } else {
        setErro(`❌ Erro no teste: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro(null);
    
    try {
      console.log("Tentando fazer login com:", { login, senha: "***" });
      
      const { data } = await api.post("/auth/login", {
        login: login.trim(),
        senha: senha.trim(),
      });
      
      console.log("Login bem-sucedido:", data);
      
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("token_type", data.token_type);
      
      navigate("/dashboard");
      
    } catch (err) {
      console.error("Erro completo:", err);
      console.error("Response data:", err.response?.data);
      console.error("Status:", err.response?.status);
      
      // Mensagens específicas baseadas no status e conteúdo da resposta
      if (err.response?.status === 401) {
        const detail = err.response?.data?.detail || "";
        if (detail.includes("não encontrado")) {
          setErro(`❌ ${detail}`);
        } else if (detail.includes("Senha incorreta")) {
          setErro(`🔑 ${detail}`);
        } else {
          setErro("🚫 Credenciais inválidas. Verifique usuário e senha.");
        }
      } else if (err.response?.status === 503) {
        setErro(`🔌 Problema de conexão: ${err.response?.data?.detail || "Banco de dados indisponível"}`);
      } else if (err.response?.status === 500) {
        setErro(`⚠️ Erro no servidor: ${err.response?.data?.detail || "Erro interno do sistema"}`);
      } else if (err.response?.status === 422) {
        setErro("📝 Dados inválidos. Verifique se os campos estão preenchidos corretamente.");
      } else if (err.code === 'ERR_NETWORK') {
        setErro("🌐 Erro de rede. Verifique sua conexão com a internet.");
      } else if (err.response?.data?.detail) {
        setErro(`💥 ${err.response.data.detail}`);
      } else {
        setErro(`❓ Erro desconhecido: ${err.message || "Tente novamente em alguns instantes"}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div 
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url('/src/imagem/login.png')" }}
    >
      {/* Overlay escuro para melhorar legibilidade */}
      <div className="absolute inset-0 bg-black opacity-30"></div>

      <div className="relative z-10 w-full max-w-sm px-6">
        <div className="bg-white/60 backdrop-blur-sm rounded-3xl shadow-xl p-8">
          {/* Ícone e título */}
          <div className="text-center mb-8">
            <div className="inline-block p-3 rounded-full bg-blue-100/50 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Transportador</h2>
            <p className="text-gray-700 mt-2">Para sua proteção, verifique sua identidade.</p>
          </div>

          {erro && (
            <div className="mb-4 p-3 bg-red-100/80 border border-red-400 text-red-700 rounded-lg">
              <p className="text-sm">{erro}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Usuário
              </label>
              <input
                className="w-full px-4 py-3 bg-white/80 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Digite seu usuário"
                value={login}
                onChange={(e) => setLogin(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Senha
              </label>
              <input
                type="password"
                className="w-full px-4 py-3 bg-white/80 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Digite sua senha"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div>
              <button 
                type="submit"
                className="w-full bg-blue-600 text-white py-3 rounded-xl font-medium hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={loading}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Entrando...
                  </span>
                ) : (
                  "Login"
                )}
              </button>
            </div>

            <div className="flex items-center justify-between text-sm pt-2">
              <Link to="/register" className="text-blue-600 hover:text-blue-800 font-medium">
                Criar conta
              </Link>
              <button 
                type="button"
                onClick={testConnection}
                className="text-green-600 hover:text-green-800 font-medium"
                disabled={loading}
              >
                🔧 Testar Conexão
              </button>
              <a href="#" className="text-blue-600 hover:text-blue-800 font-medium">
                Esqueceu sua senha?
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}