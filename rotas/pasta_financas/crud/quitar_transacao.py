from flask import Blueprint, redirect, url_for, session, flash
import sqlite3
import os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_quitar = Blueprint('quitar_transacao', __name__)

@bp_quitar.route('/<int:transacao_id>')
def iniquitacao(transacao_id):
    user_id = session['user_id']
    
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    
    # Verifica se é despesa e está aberta
    cursor.execute('SELECT tipo, status FROM transacoes WHERE id = ? AND user_id = ?', 
                   (transacao_id, user_id))
    transacao = cursor.fetchone()
    
    if transacao and transacao[0] == 'despesa' and transacao[1] == 'aberto':
        cursor.execute('UPDATE transacoes SET status = "quitado" WHERE id = ?', (transacao_id,))
        conexao.commit()
        flash('✅ Despesa quitada com sucesso!', 'success')
    else:
        flash('❌ Não foi possível quitar esta transação', 'error')
    
    conexao.close()
    return redirect(url_for('financas.inifinancas'))