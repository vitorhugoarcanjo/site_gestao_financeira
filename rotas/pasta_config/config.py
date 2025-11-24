from flask import Blueprint
from rotas.middleware.autenticacao import login_required

bp_config = Blueprint('config', __name__)

@bp_config.route('/')
@login_required
def iniconfig():
    return 'Configurações'
