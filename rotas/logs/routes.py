from flask import render_template
from rotas.logs import bp_painel_logs
from rotas.middleware.autenticacao import login_required
from rotas.middleware.permissoes import requer_master
from rotas.logs.logs_services.painel_services import LogService

@bp_painel_logs.route('/')
@login_required
@requer_master
def dashboard_logs():
    """Dashboard principal de logs"""
    stats = LogService.estatisticas()
    return render_template('logs/dashboard_geral.html', stats=stats)