from flask import Blueprint, redirect, url_for, session, flash
from rotas.middleware.autenticacao import login_required
import sqlite3, os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_delete = Blueprint('deletar_transacao', __name__)


@bp_delete.route('/<int:transacao_id>')
@login_required
def inideletar(transacao_id):
    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    cursor.execute('DELETE FROM transacoes WHERE id = ? AND user_id = ?', (transacao_id, session['user_id']))

    conexao_banco.commit()
    conexao_banco.close()

    flash('Transação excluída', 'success')
    return redirect(url_for('financas.inifinancas'))