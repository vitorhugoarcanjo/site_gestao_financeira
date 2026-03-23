from flask import Blueprint

# Blueprint principal dos logs (dashboard)
bp_painel_logs = Blueprint('painel_logs', __name__)

# Importa os blueprints específicos
from rotas.logs.logs_erros.painel_erros import bp_painel_erros
from rotas.logs.logs_acessos.painel_acessos import bp_painel_acessos
from rotas.middleware.logs_middleware import log_acesso_middleware

def importar_logs(app):
    """Função para registrar todos os blueprints de logs"""
    # Importa as rotas do dashboard DEPOIS que o blueprint foi criado
    from rotas.logs import routes
    
    # Registra TODOS os blueprints de logs
    app.register_blueprint(bp_painel_logs, url_prefix="/painel_logs")  # ← ADICIONA ESTE
    app.register_blueprint(bp_painel_erros)  # url_prefix já está no blueprint
    app.register_blueprint(bp_painel_acessos)  # url_prefix já está no blueprint
