from flask import render_template, request, jsonify
from rotas.logs import bp_painel_logs
from rotas.middleware.autenticacao import login_required
from rotas.middleware.permissoes import requer_master
from rotas.logs.logs_services.painel_services import LogService
from rotas.middleware.logs_middleware import get_client_ip  # ← IMPORTE A FUNÇÃO

@bp_painel_logs.route('/')
@login_required
@requer_master
def dashboard_logs():
    """Dashboard principal de logs"""
    stats = LogService.estatisticas()
    return render_template('logs/dashboard_geral.html', stats=stats)

# ROTA DE TESTE PARA VERIFICAR O IP
@bp_painel_logs.route('/meu-ip')
@login_required
@requer_master
def meu_ip():
    """Teste para ver o IP real do visitante"""
    info = {
        'remote_addr': request.remote_addr,
        'x_forwarded_for': request.headers.get('X-Forwarded-For'),
        'x_real_ip': request.headers.get('X-Real-IP'),
        'user_agent': request.headers.get('User-Agent'),
        'ip_real': get_client_ip()
    }
    
    # Retorna como JSON bonito
    import json
    return f"<pre>{json.dumps(info, indent=2, ensure_ascii=False)}</pre>"