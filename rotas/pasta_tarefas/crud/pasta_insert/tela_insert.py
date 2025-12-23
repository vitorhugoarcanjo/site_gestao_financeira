from flask import Blueprint, request, render_template, session, redirect, url_for
import os, sqlite3

bp_insert_tarefas = Blueprint('insert_tarefas', __name__)

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

@bp_insert_tarefas.route('/', methods=['GET', 'POST'])
def iniinsert():
    if request.method == 'POST':
        user_id = session['user_id']
        descricao = request.form.get('descricao')
        status = request.form.get('status')
        data_inicio = request.form.get('data_inicio')
        data_final = request.form.get('data_final')


        try:
            conexao_banco = sqlite3.connect(caminho_banco)
            cursor = conexao_banco.cursor()

            cursor.execute('INSERT INTO tarefas (user_id, descricao, status, data_inicio, data_final) VALUES (?, ?, ?, ?, ?)', (user_id, descricao or '', status or 'pendente', data_inicio, data_final))

            conexao_banco.commit()
            conexao_banco.close()
            return redirect(url_for('tarefas.initarefas'))


        except Exception as e:
            print(f'Erro: {e}')

    
    return render_template('pasta_tarefas/crud/tela_insert.html')