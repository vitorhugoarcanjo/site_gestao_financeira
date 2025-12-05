import sqlite3
from flask import request


def validacao_data(caminho_banco, user_id):
    data_inicio = request.args.get('data_inicio')
    data_final = request.args.get('data_final')
    descricao = request.args.get('descricao')
    tipo = request.args.get('tipo')

    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    query = 'SELECT id, tipo, valor_total, descricao, data_emissao, categoria, status, data_vencimento FROM transacoes WHERE user_id = ?'
    params = [user_id]

    if data_inicio and data_final:
        query += ' AND data_emissao BETWEEN ? AND ?'
        params.extend([data_inicio, data_final])

    # DESCRIÇÃO
    if descricao:
        query += ' AND descricao LIKE ?'
        params.append(f'%{descricao}%')

    # RECEITA OU DESPESA
    if tipo:
        query += ' AND tipo = ?'
        params.append(tipo)

    query += ' ORDER BY data_emissao DESC' # ORDENA AQUI

    cursor.execute(query, params)
    transacoes = cursor.fetchall()


    return transacoes