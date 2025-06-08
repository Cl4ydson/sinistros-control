#!/usr/bin/env python3
"""
API direta para sinistros
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from app.repositories.sinistro_repository_pyodbc import SinistroRepositoryPyODBC
from app.services.sinistro_service_pyodbc import SinistroServicePyODBC

class SinistroHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        
        try:
            path = self.path.split('?')[0]
            query_params = {}
            
            if '?' in self.path:
                query_string = self.path.split('?')[1]
                query_params = urllib.parse.parse_qs(query_string)
                # Converter listas para valores únicos
                for key, value in query_params.items():
                    if isinstance(value, list) and value:
                        query_params[key] = value[0]
            
            if path == '/':
                response = {
                    "message": "API Direta de Sinistros funcionando!",
                    "endpoints": ["/sinistros", "/test", "/health"]
                }
            
            elif path == '/health':
                response = {"status": "healthy"}
            
            elif path == '/test':
                repo = SinistroRepositoryPyODBC()
                if repo.test_connection():
                    stats = repo.obter_estatisticas()
                    response = {
                        "success": True,
                        "connection": "OK",
                        "total_sinistros": stats['total_sinistros']
                    }
                else:
                    response = {"success": False, "error": "Conexão falhou"}
            
            elif path == '/sinistros':
                service = SinistroServicePyODBC()
                
                # Parâmetros
                limit = int(query_params.get('limit', 100))
                dt_ini = query_params.get('dt_ini')
                dt_fim = query_params.get('dt_fim')
                cliente = query_params.get('cliente')
                modal = query_params.get('modal')
                
                resultado = service.listar_sinistros(
                    dt_ini=dt_ini,
                    dt_fim=dt_fim,
                    cliente=cliente,
                    modal=modal,
                    limit=limit
                )
                
                response = {
                    "success": True,
                    "data": resultado,
                    "message": f"Encontrados {resultado['total']} sinistros"
                }
            
            else:
                response = {"error": "Endpoint não encontrado"}
            
            self.wfile.write(json.dumps(response, default=str, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            error_response = {"error": str(e), "success": False}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

def run_server():
    server_address = ('127.0.0.1', 8001)
    httpd = HTTPServer(server_address, SinistroHandler)
    print(f"🚀 Servidor iniciado em http://127.0.0.1:8001")
    print("📖 Endpoints disponíveis:")
    print("  - GET /health")
    print("  - GET /test") 
    print("  - GET /sinistros")
    print("=" * 50)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server() 