import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../utils/api";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    nome: "", login: "", email: "", senha: "", setor: "",
  });
  const [msg,  setMsg]  = useState(null);
  const [erro, setErro] = useState(null);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/auth/register/", form);
      setMsg("Usuário cadastrado com sucesso! Faça login.");
      setErro(null);
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      if (err.response?.status === 409) {
        const d = err.response.data.detail;
        setErro(d === "login_duplicado"
          ? "Login já existe."
          : "E-mail já cadastrado.");
      } else if (err.response?.status === 404) {
        setErro("Endpoint não encontrado. Reinicie o backend.");
      } else {
        setErro("Falha inesperada. Tente novamente.");
      }
      setMsg(null);
    }
  };

  return (
    <div 
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url('/src/imagem/login.png')" }}
    >
      {/* Overlay escuro para melhorar legibilidade */}
      <div className="absolute inset-0 bg-black opacity-30"></div>

      <div className="relative z-10 w-full max-w-md px-6">
        <div className="bg-white/60 backdrop-blur-sm rounded-3xl shadow-xl p-8">
          {/* Ícone e título */}
          <div className="text-center mb-8">
            <div className="inline-block p-3 rounded-full bg-blue-100/50 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Criar Conta</h2>
            <p className="text-gray-700 mt-2">Preencha os dados para se cadastrar</p>
          </div>

          {msg && (
            <div className="mb-4 p-3 bg-green-100/80 border border-green-400 text-green-700 rounded-lg">
              <p className="text-sm">{msg}</p>
            </div>
          )}
          
          {erro && (
            <div className="mb-4 p-3 bg-red-100/80 border border-red-400 text-red-700 rounded-lg">
              <p className="text-sm">{erro}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nome Completo
              </label>
              <input
                className="w-full px-4 py-3 bg-white/80 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Digite seu nome"
                name="nome"
                value={form.nome}
                onChange={handleChange}
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Login
                </label>
                <input
                  className="w-full px-4 py-3 bg-white/80 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  placeholder="Escolha um login"
                  name="login"
                  value={form.login}
                  onChange={handleChange}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  E-mail
                </label>
                <input
                  className="w-full px-4 py-3 bg-white/80 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  placeholder="seu@email.com"
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Senha
                </label>
                <input
                  className="w-full px-4 py-3 bg-white/80 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  placeholder="Digite sua senha"
                  name="senha"
                  type="password"
                  value={form.senha}
                  onChange={handleChange}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Setor
                </label>
                <input
                  className="w-full px-4 py-3 bg-white/80 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  placeholder="Seu setor (opcional)"
                  name="setor"
                  value={form.setor}
                  onChange={handleChange}
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 rounded-xl font-medium hover:bg-blue-700 transition-colors duration-200 mt-6"
            >
              Cadastrar
            </button>

            <div className="text-center mt-4">
              <Link
                to="/login"
                className="text-blue-600 hover:text-blue-800 font-medium text-sm"
              >
                Já tenho uma conta
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
