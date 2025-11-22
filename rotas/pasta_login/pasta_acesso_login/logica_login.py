from flask import Flask, Blueprint, render_template, redirect, request, flash
import sqlite3, os


# VALIDAÇÃO DE LOGIN
from rotas.pasta_login.pasta_acesso_login.validacoes.validar_usuario import validar_usuario_bd

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_login = Blueprint('login', __name__)



@bp_login.route('/', methods=['GET', 'POST'])
def validar_login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    erro = []

    

    if request.method == 'POST':
        resultado = validar_usuario_bd(caminho_banco, nome, senha)

        if resultado:
            return render_template('pasta_tela_pos_login/teste.html')

        if not resultado:
            erro = 'Usuário ou senha incorretos!'
            return render_template('pasta_login/pasta_acesso_login/tela_logica_login.html', erro=erro)



    return render_template('pasta_login/pasta_acesso_login/tela_logica_login.html', nome=nome, senha=senha)