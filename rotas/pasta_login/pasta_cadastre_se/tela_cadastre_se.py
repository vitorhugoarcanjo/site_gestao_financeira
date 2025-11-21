from flask import Blueprint, request, redirect, render_template
import sqlite3, os

bp_cadastre_se = Blueprint('cadastre_se', __name__)

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

@bp_cadastre_se.route('/', methods=['GET', 'POST'])
def tela_cadastre_se():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if request.method == 'POST':
        conexao_banco = sqlite3.connect(caminho_banco)
        cursor = conexao_banco.cursor()

        cursor.execute('INSERT INTO cadastre_se (nome, telefone, email, senha) VALUES (?, ?, ?, ?)', (nome, telefone, email, senha,))

        conexao_banco.commit()
        conexao_banco.close()

        return redirect('pasta_tela_inicial/a.html')

    return render_template('pasta_login/pasta_cadastre_se/tela_cadastre_se.html')