from flask import Blueprint, render_template, session, request
from rotas.middleware.autenticacao import login_required
import sqlite3, os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_dashboard = Blueprint('dashboard', __name__)


@bp_dashboard.route('/', methods=['GET'])
@login_required
def inidashboard():
    if request.method == 'GET':
        user_id = session['user_id']
        tipo = request.args.get('tipo')

        data_inicio = request.args.get('data_inicio')
        data_final = request.args.get('data_final')

        conexao_banco = sqlite3.connect(caminho_banco)
        cursor = conexao_banco.cursor()


        query = 'SELECT SUM(valor) FROM transacoes WHERE user_id = ? AND tipo = ?'
        params_despesas = [user_id, 'despesa']
        params_receitas = [user_id, 'receita']

        if data_inicio and data_final:
            query += ' AND data BETWEEN ? AND ?'
            params_despesas.extend([data_inicio, data_final])
            params_receitas.extend([data_inicio, data_final])

        # executa para receitas
        cursor.execute(query, params_receitas)
        total_receitas = cursor.fetchone()[0] or 0

        # executa para despesas
        cursor.execute(query, params_despesas)
        total_despesas = cursor.fetchone()[0] or 0

        saldo = total_receitas - total_despesas

        return render_template('pasta_dashboard/tela_dashboard.html', total_receitas=total_receitas, total_despesas=total_despesas,
                               saldo=saldo, data_final=data_final, data_inicio=data_inicio)
    
    return render_template('pasta_dashboard/tela_dashboard.html')
