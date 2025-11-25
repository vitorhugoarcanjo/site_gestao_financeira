from flask import Blueprint, render_template
from rotas.middleware.autenticacao import login_required

bp_financas = Blueprint('financas', __name__)


@bp_financas.route('/')
@login_required
def inifinancas():
    return render_template('pasta_financas/tela_financas.html')
