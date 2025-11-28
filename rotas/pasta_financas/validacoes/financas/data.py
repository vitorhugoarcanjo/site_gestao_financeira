import sqlite3
from flask import Flask, request


def validacao_data(caminho_banco, user_id):
    data_inicio = request.args.get('data_inicio')
    data_final = request.args.get('data_final')

    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    query = 'SELECT * FROM transacoes WHERE user_id = ? AND tipo = ?'
    params_despesas = [user_id, 'despesa']
    params_receitas = [user_id, 'receita']

    if data_inicio and data_final:
        query += ' AND data BETWEEN ? AND ?'
        params_despesas.extend([data_inicio, data_final])
        params_receitas.extend([data_inicio, data_final])

    cursor.execute(query, params_despesas)
    list_despesas = cursor.fetchall()

    cursor.execute(query, params_receitas)
    list_receitas = cursor.fetchall()


    return (list_despesas, list_receitas)