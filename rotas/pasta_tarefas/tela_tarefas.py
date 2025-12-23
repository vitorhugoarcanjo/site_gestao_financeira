from flask import Blueprint, render_template, session
import os, sqlite3
from rotas.middleware.autenticacao import login_required

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_tela_tarefas = Blueprint('tarefas', __name__)

@bp_tela_tarefas.route('/', methods=['GET', 'POST'])
@login_required
def initarefas():
    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    cursor.execute('SELECT descricao, status, data_inicio, data_final FROM tarefas WHERE user_id = ?', (session['user_id'],))
    resultado_tarefas = cursor.fetchall()

    conexao_banco.close()
    

    return render_template('pasta_tarefas/tela_tarefas.html', user_nome=session.get('user_nome'), resultado_tarefas=resultado_tarefas)
