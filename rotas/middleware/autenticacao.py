from flask import session, redirect, url_for, flash
from functools import wraps

def login_required(f):
    """Decorator para verificar se usuário está logado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página', 'warning')
            return redirect(url_for('login.validar_login'))
        return f(*args, **kwargs)
    return decorated_function