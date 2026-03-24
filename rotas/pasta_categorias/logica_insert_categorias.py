import os
import sqlite3
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from rotas.middleware.autenticacao import login_required
from .tela_categorias import ini_categorias
from .crud.categorias_tarefas.cat_tarefas import insert_cat_tarefa

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')
bp_categorias = Blueprint('categorias', __name__)


@bp_categorias.route('/', methods=['GET'])
@login_required
def listar_categorias():
    return ini_categorias()

@bp_categorias.route('/novo', methods=['GET','POST'])
@login_required
def insert_categorias_global():
    msg = ''

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cor = request.form.get('cor', '').strip()
        modulo = request.form.get('modulo', '').strip()

        if not all([nome, cor]):
            msg = "Descreva todos os campos corretamente!"
            return render_template('pasta_categorias/crud/insert_categorias.html', msg=msg)
        
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()
        user_id = session['user_id']

        if modulo == 'tarefas':
            ok, msg = insert_cat_tarefa(nome, cor, user_id, cursor)

        else:
            msg = "Módulo inválido"
            return render_template('pasta_categorias/crud/insert_categorias.html', msg=msg)

        if ok:
            conexao.commit()
            conexao.close()
            return redirect(url_for('categorias.listar_categorias'))

        else:
            conexao.rollback()
            conexao.close()  # ← LINHA 2: FECHA!
            msg = msg or "Erro ao criar categoria"
            return render_template('pasta_categorias/crud/insert_categorias.html', msg=msg)  # ← LINHA 3: MOSTRA MSG!
    
    return render_template('pasta_categorias/crud/insert_categorias.html')


@bp_categorias.route('/excluir/<int:id>')
@login_required
def excluir_categoria(id):
    user_id = session['user_id']
    
    with sqlite3.connect(caminho_banco) as conexao:
        cursor = conexao.cursor()
        
        # Exclui a categoria
        cursor.execute("DELETE FROM categorias_tarefas WHERE id = ? AND user_id = ?", (id, user_id))
        
        conexao.commit()
    
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('categorias.listar_categorias'))