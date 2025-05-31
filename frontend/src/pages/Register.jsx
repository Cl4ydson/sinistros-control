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
    <div className="flex items-center justify-center h-screen bg-gray-200">
      <form className="bg-white shadow-md rounded p-8 w-96" onSubmit={handleSubmit}>
        <h2 className="text-2xl mb-4 text-center">Criar Conta</h2>
        {msg  && <p className="text-green-700 mb-2 text-center">{msg}</p>}
        {erro && <p className="text-red-500 mb-2 text-center">{erro}</p>}

        <div className="grid grid-cols-2 gap-3">
          <input className="p-2 border rounded col-span-2" placeholder="Nome"
                 name="nome"  value={form.nome}  onChange={handleChange} required />
          <input className="p-2 border rounded" placeholder="Login"
                 name="login" value={form.login} onChange={handleChange} required />
          <input className="p-2 border rounded" placeholder="E-mail"
                 name="email" value={form.email} onChange={handleChange} required />
          <input type="password" className="p-2 border rounded" placeholder="Senha"
                 name="senha" value={form.senha} onChange={handleChange} required />
          <input className="p-2 border rounded" placeholder="Setor (opcional)"
                 name="setor" value={form.setor} onChange={handleChange} />
        </div>

        <button className="w-full bg-blue-600 text-white py-2 rounded mt-4">
          Cadastrar
        </button>

        <Link to="/login"
              className="text-sm text-blue-600 hover:underline block text-center mt-2">
          Já tenho conta
        </Link>
      </form>
    </div>
  );
}
