from flask import Blueprint, request, redirect, render_template, url_for, flash
import os, sqlite3


from .validacoes.criptografia_snh import criptografar_senha
from .validacoes.validar_usuario import (
    validar_email_formato,
    validar_email_unico,
    validar_senha_tamanho,
    validar_campos_obrigatorios,
    validar_confirmacao_senha,
    validar_e_limpar_telefone
)

bp_cadastre_se = Blueprint('cadastre_se', __name__)
caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

@bp_cadastre_se.route('/', methods=['GET', 'POST'])
def tela_cadastre_se():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')


        # VALIDA TELEFONE
        telefone_limpo = validar_e_limpar_telefone(telefone)
        if not telefone_limpo:
            return redirect(url_for('cadastre_se.tela_cadastre_se'))


        # SENHA CRIPTOGRAFADA
        senha_criptografada = criptografar_senha(senha)

        if not all([
            validar_campos_obrigatorios(nome, telefone, email, senha, confirmar_senha),
            validar_confirmacao_senha(senha, confirmar_senha),
            validar_email_formato(email),
            validar_senha_tamanho(senha),
            validar_email_unico(caminho_banco, email)
        ]):
            return redirect(url_for('cadastre_se.tela_cadastre_se'))


        # SE PASSOU NAS VALIDAÇÕES: FAZ INSERT
        try:
            conexao_banco = sqlite3.connect(caminho_banco)
            cursor = conexao_banco.cursor()

            cursor.execute('INSERT INTO cadastre_se (nome, telefone, email, senha) VALUES (?, ?, ?, ?)', (nome, telefone_limpo, email, senha_criptografada))
            conexao_banco.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login.validar_login'))
        
        except Exception as e:
            flash('Erro ao cadastrar: ' + str(e), 'error')

        finally:
            conexao_banco.close()

    return render_template('pasta_login/pasta_cadastre_se/tela_cadastre_se.html')