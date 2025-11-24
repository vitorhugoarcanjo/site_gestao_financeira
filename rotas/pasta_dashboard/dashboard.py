from flask import Blueprint, render_template

from rotas.middleware.autenticacao import login_required

bp_dashboard = Blueprint('dashboard', __name__)


@bp_dashboard.route('/')
@login_required
def inidashboard():
    return 'Olá Dashboard'
