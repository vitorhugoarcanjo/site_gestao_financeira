from flask import Blueprint, render_template, session, redirect, url_for, flash
import os, sqlite3
from rotas.middleware.autenticacao import login_required

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_tela_tarefas = Blueprint('tarefas', __name__)

@bp_tela_tarefas.route('/', methods=['GET', 'POST'])
@login_required
def ini_tarefas():
    with sqlite3.connect(caminho_banco) as conexao_banco:
        cursor = conexao_banco.cursor()

        cursor.execute("""SELECT t.tarefa_sequencia, t.descricao, t.status, t.data_inicio, t.data_final, t.categoria_id, t.prioridade,
                       c.nome as categoria_nome, c.cor as categoria_cor
                    FROM tarefas t 
                    LEFT JOIN categorias_tarefas c ON t.categoria_id = c.id   
                    WHERE t.user_id = ?
                    ORDER BY t.tarefa_sequencia ASC
                    """, (session['user_id'],))
        tarefas = cursor.fetchall()
    return render_template('pasta_tarefas/tela_tarefas.html.jinja', user_nome=session.get('user_nome'), tarefas=tarefas)



# FUNÇÃO DE CONCLUIR TAREFA
@bp_tela_tarefas.route('/concluir/<int:tarefa_seq>', methods=['POST'])
@login_required
def concluir_tarefa(tarefa_seq):
    with sqlite3.connect(caminho_banco) as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('UPDATE tarefas SET status = ? WHERE tarefa_sequencia = ? AND user_id = ?', ('concluido', tarefa_seq, session['user_id']))
        conexao.commit()

        flash('Tarefa concluída com sucesso!', 'success')
        return redirect(url_for('tarefas.ini_tarefas'))




# FUNÇÃO PARA EXCLUIR TAREFA
@bp_tela_tarefas.route('/excluir/<int:tarefa_seq>', methods=['POST'])
@login_required
def excluir_tarefa(tarefa_seq):
    with sqlite3.connect(caminho_banco) as conexao:
        cursor = conexao.cursor()

        cursor.execute('DELETE FROM tarefas WHERE tarefa_sequencia = ? AND user_id = ?', (tarefa_seq, session['user_id'] ))

        conexao.commit()

        flash('Tarefa excluída com sucesso!', 'success')
        return redirect(url_for('tarefas.ini_tarefas'))
