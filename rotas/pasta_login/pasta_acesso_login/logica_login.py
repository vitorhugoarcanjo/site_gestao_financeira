""" LÓGICA DO LOGIN  - INICIO """
import os
import sqlite3
from flask import Blueprint, render_template, redirect, request, flash, url_for, session


# VALIDAÇÃO DE LOGIN
from rotas.pasta_login.pasta_acesso_login.validacoes.validar_usuario import validar_usuario_bd

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_login = Blueprint('login', __name__)


@bp_login.route('/', methods=['GET', 'POST'])
def validar_login():
    """ INICIO DA VALIDAÇÃO """
    if request.method == 'POST':
        nome_ou_email = request.form.get('nome_ou_email')
        senha = request.form.get('senha')

        # VALIDAÇÃO 1
        if not nome_ou_email or not senha:
            flash('Preencha todos os campos!', 'warning')
            return redirect(url_for('login.validar_login'))

        # PRIMEIRO: VERIFICA SE O USUÁRIO EXISTE E SE O EMAIL FOI CONFIRMADO
        with sqlite3.connect(caminho_banco) as conexao_banco:
            cursor = conexao_banco.cursor()
            cursor.execute('SELECT id, nome, email_verificado FROM cadastre_se WHERE (nome = ? OR email = ?)',
                           (nome_ou_email, nome_ou_email))
            usuario = cursor.fetchone()
            
            if not usuario:
                flash('Usuário não encontrado!', 'error')
                return redirect(url_for('login.validar_login'))
            
            # VERIFICA SE EMAIL FOI CONFIRMADO
            if usuario[2] != 1:  # email_verificado = 0
                flash('Email não confirmado! Verifique sua caixa de entrada.', 'warning')
                return redirect(url_for('cadastre_se.confirmar_email', user_id=usuario[0]))

        # SEGUNDO: VALIDA SENHA
        resultado = validar_usuario_bd(caminho_banco, nome_ou_email, senha)

        if resultado:
            # SETAR NA SESSÃO
            session.permanent = True
            session['user_id'] = usuario[0]
            session['user_nome'] = usuario[1]

            flash('Logado com sucesso!', 'success')
            return redirect(url_for('pos_login.iniposlogin'))
        else:
            flash('Senha incorreta!', 'error')
            return redirect(url_for('login.validar_login'))

    return render_template('pasta_login/pasta_acesso_login/tela_logica_login.html')