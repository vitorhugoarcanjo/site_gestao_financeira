from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from rotas.middleware.autenticacao import login_required
import os, sqlite3

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_insert_transacao = Blueprint('nova_transacao', __name__)

@bp_insert_transacao.route('/', methods=['GET', 'POST'])
@login_required
def initransacao():
    if request.method == 'POST':
        user_id = session['user_id']
        tipo = request.form.get('tipo')
        valor = float(request.form.get('valor'))
        descricao = request.form.get('descricao')
        data = request.form.get('data')
        
        # INSERT SIMPLES
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO transacoes (user_id, tipo, valor, descricao, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, tipo, valor, descricao, data))
        conexao.commit()
        conexao.close()
        
        flash('Transação salva!', 'success')
        return redirect(url_for('financas.inifinancas'))
    
    return render_template('pasta_financas/crud/insert_transacao.html')