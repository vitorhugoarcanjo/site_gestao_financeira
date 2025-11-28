from flask import Blueprint, redirect, render_template, url_for, request, session, flash
from rotas.middleware.autenticacao import login_required
import sqlite3, os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_edit_transacao = Blueprint('edit_transacoes', __name__)


@bp_edit_transacao.route('/<int:transacao_id>', methods=['GET', 'POST'])
@login_required
def inieditar(transacao_id):

    if request.method == 'GET':
        conexao_banco = sqlite3.connect(caminho_banco)
        cursor = conexao_banco.cursor()

        cursor.execute('SELECT * FROM transacoes WHERE id = ? AND user_id = ?', (transacao_id, session['user_id']))
        transacao = cursor.fetchone()
        conexao_banco.close()

        return render_template('pasta_financas/crud/edit_transacao.html', transacao=transacao, transacao_id=transacao_id)
    
    if request.method == 'POST':
        user_id = session['user_id']
        descricao = request.form.get('descricao')
        valor = float(request.form.get('valor'))
        tipo = request.form.get('tipo')
        data = request.form.get('data')

        conexao_banco = sqlite3.connect(caminho_banco)
        cursor = conexao_banco.cursor()

        cursor.execute('UPDATE transacoes SET descricao = ?, valor = ?, tipo = ?, data = ? WHERE id = ? AND user_id = ?', (descricao, valor, tipo, data, transacao_id, user_id))

        conexao_banco.commit()
        conexao_banco.close()

        flash('Atualizado com sucesso!', 'success')
        return redirect(url_for('financas.inifinancas'))
    

    return render_template('pasta_financas/crud/edit_transacao.html')





