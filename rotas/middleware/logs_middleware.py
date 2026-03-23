# rotas/middleware/logs_middleware.py
import time
from flask import request, session, g
from rotas.logs.logs_services.painel_services import LogService

# Rotas que NÃO DEVEM ser logadas
ROTAS_IGNORADAS = [
    '/static',
    '/favicon.ico',
    '/robots.txt',
    '/painel_logs',
    '/logs_erros',
    '/painel_acessos',
]

# PADRÕES DE ATAQUE PARA IGNORAR (não registrar no banco)
PADROES_ATAQUE = [
    '.env', '.git', '.svn', '.htaccess',
    'wp-', 'wordpress', 'wlwmanifest', 'xmlrpc',
    'joomla', 'drupal', 'magento',
    'Dr0v', 'wp-includes', 'wp-content',
    'config', 'settings', 'setup', 'backup',
    'phpmyadmin', 'mysql', 'admin', 'login'
]

def get_client_ip():
    """Tenta obter o IP real do cliente considerando proxies"""
    headers = [
        'X-Forwarded-For',
        'X-Real-IP',
        'CF-Connecting-IP',
        'True-Client-IP'
    ]
    
    for header in headers:
        ip = request.headers.get(header)
        if ip:
            return ip.split(',')[0].strip()
    
    return request.remote_addr

def log_acesso_middleware(app):
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if not hasattr(g, 'start_time'):
            return response
        
        tempo_resposta = int((time.time() - g.start_time) * 1000)
        
        # Ignora rotas que não precisam de log
        for rota in ROTAS_IGNORADAS:
            if request.path.startswith(rota):
                return response
        
        # IGNORA PADRÕES DE ATAQUE (não registra no banco)
        caminho = request.path.lower()
        for padrao in PADROES_ATAQUE:
            if padrao in caminho:
                return response
        
        # Ignora redirecionamentos comuns
        if response.status_code == 302 and request.path == '/pos_login/':
            return response
        
        # Só loga se for GET ou POST
        if request.method not in ['GET', 'POST']:
            return response
        
        user_id = session.get('user_id')
        ip = get_client_ip()
        
        # Registra o acesso
        LogService.registrar_acesso(
            user_id=user_id,
            ip=ip,
            user_agent=request.headers.get('User-Agent', '')[:500],
            rota=request.path[:255],
            metodo=request.method,
            status_code=response.status_code,
            tempo_resposta=tempo_resposta
        )
        
        return response