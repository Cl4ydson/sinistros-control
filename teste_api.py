"""
Script para testar e debugar a API de sinistros
"""

import requests
import json
from datetime import date, datetime, timedelta

class TesteAPI:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
    
    def fazer_login(self, username="admin", password="admin"):
        """Faz login e obtém token"""
        print("🔐 Fazendo login...")
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={"login": username, "senha": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print("✅ Login realizado com sucesso!")
                return True
            else:
                print(f"❌ Erro no login: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao fazer login: {e}")
            return False
    
    def testar_conexao_api(self):
        """Testa se a API está respondendo"""
        print("🌐 Testando conexão com API...")
        
        try:
            response = self.session.get(f"{self.base_url}/")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def testar_endpoint_sinistros(self):
        """Testa especificamente o endpoint de sinistros"""
        print("\n🔍 Testando endpoint de sinistros...")
        
        endpoints = [
            "/sinistros/",
            "/sinistros/buscar",
            "/sinistros/listar"
        ]
        
        for endpoint in endpoints:
            try:
                print(f"\n📡 Testando: {endpoint}")
                response = self.session.get(f"{self.base_url}{endpoint}")
                
                print(f"   Status: {response.status_code}")
                print(f"   Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   Dados: {type(data)}")
                        
                        if isinstance(data, list):
                            print(f"   Quantidade: {len(data)} registros")
                            if data:
                                print(f"   Primeiro registro: {data[0]}")
                        elif isinstance(data, dict):
                            print(f"   Chaves: {list(data.keys())}")
                        else:
                            print(f"   Conteúdo: {data}")
                            
                    except json.JSONDecodeError:
                        print(f"   Response não é JSON: {response.text[:200]}...")
                else:
                    print(f"   Erro: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
    
    def testar_com_parametros(self):
        """Testa endpoint com diferentes parâmetros"""
        print("\n🔧 Testando com parâmetros...")
        
        # Assumindo que o endpoint aceita parâmetros via GET
        parametros_teste = [
            {},  # Sem parâmetros
            {"limit": 5},  # Com limite
            {"limit": 10, "offset": 0},  # Com limite e offset
            {"dt_ini": "2024-01-01", "dt_fim": "2024-12-31"},  # Com datas
        ]
        
        for params in parametros_teste:
            try:
                print(f"\n📊 Testando com parâmetros: {params}")
                response = self.session.get(f"{self.base_url}/sinistros/", params=params)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   ✅ Retornados: {len(data)} registros")
                            if data:
                                print(f"   Primeiro: {list(data[0].keys()) if isinstance(data[0], dict) else data[0]}")
                        else:
                            print(f"   Tipo: {type(data)}")
                    except:
                        print(f"   Response: {response.text[:100]}...")
                else:
                    print(f"   ❌ Erro: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
    
    def testar_com_post(self):
        """Testa endpoint via POST (caso seja necessário)"""
        print("\n📤 Testando via POST...")
        
        payloads = [
            {},  # Vazio
            {"limit": 5},  # Com limite
            {"filters": {"limit": 10}},  # Com filtros
        ]
        
        for payload in payloads:
            try:
                print(f"\n📊 POST com payload: {payload}")
                response = self.session.post(f"{self.base_url}/sinistros/", json=payload)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   ✅ Retornados: {len(data)} registros")
                        else:
                            print(f"   Tipo: {type(data)}")
                    except:
                        print(f"   Response: {response.text[:100]}...")
                else:
                    print(f"   ❌ Erro: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
    
    def testar_docs_api(self):
        """Testa acesso à documentação da API"""
        print("\n📚 Testando documentação da API...")
        
        docs_endpoints = [
            "/docs",
            "/redoc",
            "/openapi.json"
        ]
        
        for endpoint in docs_endpoints:
            try:
                print(f"\n📖 Testando: {endpoint}")
                response = self.session.get(f"{self.base_url}{endpoint}")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ Documentação disponível em: {self.base_url}{endpoint}")
                else:
                    print(f"   ❌ Não disponível")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
    
    def testar_endpoints_alternativos(self):
        """Testa outros endpoints que podem existir"""
        print("\n🔄 Testando endpoints alternativos...")
        
        endpoints_alternativos = [
            "/api/sinistros/",
            "/v1/sinistros/",
            "/sinistros/all",
            "/sinistros/search",
            "/claims/",
            "/incidents/"
        ]
        
        for endpoint in endpoints_alternativos:
            try:
                print(f"\n🔍 Testando: {endpoint}")
                response = self.session.get(f"{self.base_url}{endpoint}")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ Endpoint encontrado!")
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   Registros: {len(data)}")
                        elif isinstance(data, dict):
                            print(f"   Chaves: {list(data.keys())}")
                    except:
                        print(f"   Response: {response.text[:100]}...")
                elif response.status_code == 404:
                    print(f"   ❌ Não encontrado")
                else:
                    print(f"   ⚠️ Status: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
    
    def verificar_banco_dados(self):
        """Verifica se há dados no banco através da API"""
        print("\n💾 Verificando dados no banco...")
        
        # Tenta diferentes abordagens para acessar dados
        endpoints_dados = [
            "/sinistros/count",
            "/sinistros/total",
            "/sinistros/stats",
            "/health",
            "/status"
        ]
        
        for endpoint in endpoints_dados:
            try:
                print(f"\n📊 Testando: {endpoint}")
                response = self.session.get(f"{self.base_url}{endpoint}")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   ✅ Dados: {data}")
                    except:
                        print(f"   Response: {response.text[:100]}...")
                        
            except Exception as e:
                print(f"   ❌ Erro: {e}")
    
    def testar_com_diferentes_headers(self):
        """Testa com diferentes headers HTTP"""
        print("\n🏷️ Testando com diferentes headers...")
        
        headers_teste = [
            {"Content-Type": "application/json"},
            {"Accept": "application/json"},
            {"Content-Type": "application/json", "Accept": "application/json"},
            {"X-Requested-With": "XMLHttpRequest"}
        ]
        
        for headers in headers_teste:
            try:
                print(f"\n📤 Testando com headers: {headers}")
                
                # Salva headers originais
                original_headers = dict(self.session.headers)
                
                # Adiciona novos headers
                self.session.headers.update(headers)
                
                response = self.session.get(f"{self.base_url}/sinistros/")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   ✅ Retornados: {len(data)} registros")
                        else:
                            print(f"   Tipo: {type(data)}")
                    except:
                        print(f"   Response: {response.text[:100]}...")
                else:
                    print(f"   ❌ Erro: {response.text[:100]}...")
                
                # Restaura headers originais
                self.session.headers = original_headers
                
            except Exception as e:
                print(f"   ❌ Erro: {e}")
    
    def executar_todos_testes(self):
        """Executa todos os testes disponíveis"""
        print("🚀 Iniciando bateria completa de testes...\n")
        
        # Testa conexão básica
        if not self.testar_conexao_api():
            print("❌ API não está respondendo. Verifique se o servidor está rodando.")
            return
        
        # Tenta fazer login
        self.fazer_login()
        
        # Executa todos os testes
        self.testar_docs_api()
        self.testar_endpoint_sinistros()
        self.testar_endpoints_alternativos()
        self.testar_com_parametros()
        self.testar_com_post()
        self.testar_com_diferentes_headers()
        self.verificar_banco_dados()
        
        print("\n✅ Testes concluídos!")
    
    def debug_resposta_detalhada(self, endpoint="/sinistros/"):
        """Faz debug detalhado de uma resposta específica"""
        print(f"\n🔬 Debug detalhado para: {endpoint}")
        
        try:
            response = self.session.get(f"{self.base_url}{endpoint}")
            
            print(f"Status Code: {response.status_code}")
            print(f"Status Text: {response.reason}")
            print(f"Headers: {dict(response.headers)}")
            print(f"URL: {response.url}")
            print(f"Encoding: {response.encoding}")
            print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"Content-Length: {response.headers.get('content-length', 'N/A')}")
            
            print(f"\nResponse Text (primeiros 500 chars):")
            print(response.text[:500])
            
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    data = response.json()
                    print(f"\nJSON parsed successfully!")
                    print(f"Type: {type(data)}")
                    
                    if isinstance(data, list):
                        print(f"Length: {len(data)}")
                        if data:
                            print(f"First item: {data[0]}")
                    elif isinstance(data, dict):
                        print(f"Keys: {list(data.keys())}")
                        
                except json.JSONDecodeError as e:
                    print(f"\n❌ JSON decode error: {e}")
            
        except Exception as e:
            print(f"❌ Erro no debug: {e}")


def main():
    """Função principal para executar os testes"""
    print("=" * 60)
    print("🔧 TESTE E DEBUG DA API DE SINISTROS")
    print("=" * 60)
    
    # Cria instância do testador
    testador = TesteAPI()
    
    # Menu interativo
    while True:
        print("\n" + "=" * 40)
        print("Escolha uma opção:")
        print("1. Executar todos os testes")
        print("2. Testar conexão básica")
        print("3. Testar endpoint principal")
        print("4. Debug detalhado")
        print("5. Testar com parâmetros")
        print("6. Verificar documentação")
        print("7. Sair")
        print("=" * 40)
        
        try:
            opcao = input("Digite sua opção (1-7): ").strip()
            
            if opcao == "1":
                testador.executar_todos_testes()
            elif opcao == "2":
                testador.testar_conexao_api()
            elif opcao == "3":
                testador.testar_endpoint_sinistros()
            elif opcao == "4":
                endpoint = input("Digite o endpoint para debug (ex: /sinistros/): ").strip()
                if not endpoint:
                    endpoint = "/sinistros/"
                testador.debug_resposta_detalhada(endpoint)
            elif opcao == "5":
                testador.testar_com_parametros()
            elif opcao == "6":
                testador.testar_docs_api()
            elif opcao == "7":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n👋 Interrompido pelo usuário!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()