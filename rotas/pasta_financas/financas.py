from flask import Blueprint
from rotas.middleware.autenticacao import login_required

bp_financas = Blueprint('financas', __name__)


@bp_financas.route('/')
@login_required
def inifinancas():
    return 'Finanças ok'
