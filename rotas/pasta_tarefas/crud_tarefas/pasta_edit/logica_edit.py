from flask import Blueprint, render_template, request, session, redirect, url_for
import sqlite3, os

from rotas.middleware.autenticacao import login_required

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_tela_edit = Blueprint('editar_tarefa', __name__)


@bp_tela_edit.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
@login_required
def iniedittarefa(tarefa_id):
    user_id = session['user_id']

    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    cursor.execute("""SELECT t.descricao, t.status, t.data_inicio, t.data_final, t.categoria_id, t.prioridade, c.nome as categoria_nome, c.cor as categoria_cor
                   FROM tarefas t
                   LEFT JOIN categorias_tarefas c ON t.categoria_id = c.id
                   WHERE t.id = ? AND t.user_id = ?""", (tarefa_id, user_id))
    tarefa = cursor.fetchone()

    cursor.execute("""SELECT id, nome, cor FROM categorias_tarefas WHERE user_id = ?""", (user_id,))
    todas_categorias = cursor.fetchall()


    if request.method == 'POST':
        descricao = request.form.get('descricao', '')  # ← .get() evita 400
        status = request.form.get('status', '')
        data_inicio = request.form.get('data_inicio', '')
        data_final = request.form.get('data_final', '')
        categoria_id = request.form.get('categoria_id', '')
        prioridade = request.form.get('prioridade')


        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        cursor.execute('UPDATE tarefas SET descricao = ?, status = ?, data_inicio = ?, data_final = ?, categoria_id = ?, prioridade = ? WHERE id = ? AND user_id = ?', 
                       (descricao, status, data_inicio, data_final, categoria_id, prioridade, tarefa_id, user_id))
        
        conexao.commit()
        conexao.close()
        return redirect(url_for('tarefas.ini_tarefas'))
    

    if not tarefa:
        conexao.close()
        return redirect(url_for('tarefas.ini_tarefas'))

    conexao.close()
    return render_template('pasta_tarefas/crud_tarefas/tela_edit.html', tarefa=tarefa, tarefa_id=tarefa_id, todas_categorias=todas_categorias)



