import sqlite3, os
from flask import request, render_template

def validar_usuario_bd(caminho_banco, nome, senha):

    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    cursor.execute('SELECT nome, senha FROM cadastre_se WHERE nome = ? AND senha = ?', (nome, senha,))
    resultado = cursor.fetchone()

    conexao_banco.close()

    if not resultado:
        return False

    if resultado:
        return True

    
