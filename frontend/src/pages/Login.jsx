import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export default function Login() {
  const [login, setLogin] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro(null);
    
    try {
      console.log("Tentando fazer login com:", { login, senha: "***" });
      
      const { data } = await axios.post("http://localhost:8000/auth/login", {
        login: login.trim(),
        senha: senha.trim(),
      });
      
      console.log("Login bem-sucedido:", data);
      
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("token_type", data.token_type);
      
      // Usar navigate em vez de window.location.href
      navigate("/dashboard"); // ou a rota que você quiser redirecionar
      
    } catch (err) {
      console.error("Erro completo:", err);
      console.error("Response data:", err.response?.data);
      console.error("Status:", err.response?.status);
      
      if (err.response?.status === 401) {
        setErro("Login ou senha incorretos");
      } else if (err.response?.status === 422) {
        setErro("Dados inválidos. Verifique os campos.");
      } else if (err.code === 'ERR_NETWORK') {
        setErro("Erro de conexão. Verifique se o servidor está rodando na porta 8000.");
      } else {
        setErro(`Erro: ${err.response?.data?.detail || "Erro interno"}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-200">
      <form
        className="bg-white shadow-md rounded p-8 w-80"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl mb-4 text-center">Login</h2>
        {erro && <p className="text-red-500 mb-2 text-sm">{erro}</p>}
        
        <input
          className="w-full mb-3 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Usuário"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          required
          disabled={loading}
        />
        
        <input
          type="password"
          className="w-full mb-4 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          required
          disabled={loading}
        />
        
        <button 
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded mb-2 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading}
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
        
        <Link
          to="/register"
          className="text-sm text-blue-600 hover:underline block text-center"
        >
          Criar conta
        </Link>
      </form>
    </div>
  );
}