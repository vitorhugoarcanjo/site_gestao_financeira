from flask import Blueprint, render_template, session, request
import sqlite3
import os
from rotas.middleware.autenticacao import login_required


# FUNÇÃO PARA VALIDAÇÃO DATA E TIPO
from rotas.pasta_financas.validacoes.financas.data import validacao_data


bp_financas = Blueprint('financas', __name__)
caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

@bp_financas.route('/')
@login_required
def inifinancas():
    user_id = session['user_id']

    # pega filtros diretamente
    data_inicio = request.args.get('data_inicio')
    data_final = request.args.get('data_final')
    descricao = request.args.get('descricao')
    tipo = request.args.get('tipo')


    if data_inicio or data_final or descricao or tipo:
        transacoes = validacao_data(caminho_banco, user_id)


    # Se não veio filtrado, busca tudo
    else:
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        cursor.execute('''
            SELECT id, tipo, valor, descricao, data, categoria, status
            FROM transacoes 
            WHERE user_id = ? 
            ORDER BY data DESC
        ''', (user_id,))


        transacoes = cursor.fetchall()
        conexao.close()


    
    return render_template('pasta_financas/tela_financas.html', transacoes=transacoes, user_nome=session.get('user_nome'))