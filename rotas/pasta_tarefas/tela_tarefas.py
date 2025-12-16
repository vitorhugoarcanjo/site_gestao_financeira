from flask import Blueprint, render_template, request, redirect, url_for, session
from rotas.middleware.autenticacao import login_required

bp_tela_tarefas = Blueprint('tarefas', __name__)

@bp_tela_tarefas.route('/')
@login_required
def initarefas():





    return render_template('pasta_tarefas/tela_tarefas.html', user_nome=session.get('user_nome'))
