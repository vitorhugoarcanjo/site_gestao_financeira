# rotas/middleware/logs_middleware.py
import time
from flask import request, session, g
from rotas.logs.logs_services.painel_services import LogService

def log_acesso_middleware(app):
    """Middleware para registrar acessos automaticamente"""
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            tempo_resposta = int((time.time() - g.start_time) * 1000)
            
            # Ignora logs estáticos
            if request.path.startswith('/static'):
                return response
            
            # Registra o acesso
            LogService.registrar_acesso(
                usuario_id=session.get('usuario_id'),
                ip=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                rota=request.path,
                metodo=request.method,
                status_code=response.status_code,
                tempo_resposta=tempo_resposta
            )
        
        return response