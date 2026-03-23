from flask import render_template, Blueprint, request
from rotas.middleware.autenticacao import login_required
from rotas.middleware.permissoes import requer_master
from rotas.logs.logs_services.painel_services import LogService

bp_painel_acessos = Blueprint('painel_acessos', __name__, url_prefix='/painel_acessos')

@bp_painel_acessos.route('/')
@login_required
@requer_master
def logs_acessos():
    """Lista de acessos ao sistema"""
    pagina = request.args.get('pagina', 1, type=int)
    limite = 20
    offset = (pagina - 1) * limite
    filtro = request.args.get('filtro', '')
    
    resultados = LogService.listar_acessos(limite, offset, filtro)
    
    return render_template(
        'logs/pasta_logs_acessos/logs_acessos.html',
        acessos=resultados['dados'],
        total=resultados['total'],
        pagina=pagina,
        limite=limite,
        filtro=filtro
    )

@bp_painel_acessos.route('/<int:acesso_id>')
@login_required
@requer_master
def detalhe_acesso(acesso_id):
    """Detalhe de um acesso específico"""
    acesso = LogService.obter_acesso_por_id(acesso_id)
    
    if not acesso:
        return "Acesso não encontrado", 404
    
    return render_template('logs/pasta_logs_acessos/detalhe_acesso.html', acesso=acesso)