from flask import Blueprint, render_template
from rotas.middleware.autenticacao import login_required
from rotas.middleware.permissoes import requer_master
from rotas.logs.logs_services.painel_services import LogService

bp_painel_ataques = Blueprint('logs_ataques', __name__, url_prefix='/logs_ataques')

@bp_painel_ataques.route('/')
@login_required
@requer_master
def ataques():
    """Lista de tentativas de ataque"""
    ataques = LogService.listar_ataques()
    return render_template('logs/pasta_logs_ataques/ataques.html', ataques=ataques)

@bp_painel_ataques.route('/<int:ataque_id>')
@login_required
@requer_master
def detalhe_ataque(ataque_id):
    """Detalhe de uma tentativa de ataque"""
    ataque = LogService.obter_ataque_por_id(ataque_id)
    
    if not ataque:
        return "Ataque não encontrado", 404
    
    return render_template('logs/pasta_logs_ataques/detalhe_ataque.html', ataque=ataque)