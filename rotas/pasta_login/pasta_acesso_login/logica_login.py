from flask import Flask, Blueprint, render_template, redirect, request, url_for
import sqlite3, os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_login = Blueprint('login', __name__)



@bp_login.route('/', methods=['GET', 'POST'])
def validar_login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    if request.method == 'GET':

        conexao_banco = sqlite3.connect(caminho_banco)
        cursor = conexao_banco.cursor()

        cursor.execute('SELECT nome, senha FROM cadastre_se WHERE nome=? AND senha=?', (nome, senha))

        return render_template('pasta_tela_pos_login/teste.html')





    return render_template('pasta_login/pasta_acesso_login/tela_logica_login.html', nome=nome, senha=senha)