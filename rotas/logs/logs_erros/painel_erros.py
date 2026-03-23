import os
import sqlite3
from flask import render_template, Blueprint, request
from rotas.middleware.autenticacao import login_required
from rotas.middleware.permissoes import requer_master
from rotas.logs.logs_services.painel_services import LogService

bp_painel_erros = Blueprint('logs_erros', __name__, url_prefix='/logs_erros')

@bp_painel_erros.route('/')
@login_required
@requer_master
def logs_erros():
    """Lista de erros do sistema"""
    pagina = request.args.get('pagina', 1, type=int)
    limite = 20
    offset = (pagina - 1) * limite
    filtro = request.args.get('filtro', '')
    
    resultados = LogService.listar_erros(limite, offset, filtro)
    
    return render_template(
        'logs/pasta_logs_erros/logs_erros.html',
        erros=resultados['dados'],
        total=resultados['total'],
        pagina=pagina,
        limite=limite,
        filtro=filtro
    )

@bp_painel_erros.route('/<int:erro_id>')
@login_required
@requer_master
def detalhe_erro(erro_id):
    """Detalhe de um erro específico"""
    erro = LogService.obter_erro_por_id(erro_id)
    
    if not erro:
        return "Erro não encontrado", 404
    
    return render_template('logs/pasta_logs_erros/logs_erros_detalhado.html', erro=erro)