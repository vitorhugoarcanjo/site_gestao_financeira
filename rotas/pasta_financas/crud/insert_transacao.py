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
        valor_total = float(request.form.get('valor_total'))
        descricao = request.form.get('descricao')
        data_emissao = request.form.get('data_emissao')
        data_vencimento = request.form.get('data_vencimento')
        total_parcelas = request.form.get('total_parcelas', '1')
        status = 'recebido' if tipo == 'receita' else 'aberto'
        
        # INSERT SIMPLES
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO transacoes (user_id, tipo, valor_total, descricao, data_emissao, data_vencimento, total_parcelas, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, tipo, valor_total, descricao, data_emissao, data_vencimento, total_parcelas, status))
        conexao.commit()
        conexao.close()
        
        flash('Transação salva!', 'success')
        return redirect(url_for('financas.inifinancas'))
    
    return render_template('pasta_financas/crud/insert_transacao.html')