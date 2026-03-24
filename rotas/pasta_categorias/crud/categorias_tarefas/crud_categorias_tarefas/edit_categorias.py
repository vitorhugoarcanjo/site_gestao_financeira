import os
import sqlite3
from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from rotas.middleware.autenticacao import login_required

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

bp_edit_cat_tar = Blueprint('edit_cat_tar', __name__)

@bp_edit_cat_tar.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def ini_edit_cat_tar(id):
    user_id = session['user_id']
    msg = None
    categoria = None

    # Busca os dados da categoria atual
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT id, nome, cor FROM categorias_tarefas 
        WHERE id = ? AND user_id = ?
    """, (id, user_id))
    categoria = cursor.fetchone()
    conexao.close()

    if not categoria:
        flash('Categoria não encontrada!', 'danger')
        return redirect(url_for('categorias.listar_categorias'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        cor = request.form.get('cor')

        # Validação correta
        if not nome or not cor:
            msg = 'Preencha nome e cor corretamente.'
        else:
            try:
                conexao = sqlite3.connect(caminho_banco)
                cursor = conexao.cursor()

                # UPDATE, não INSERT
                cursor.execute("""
                    UPDATE categorias_tarefas 
                    SET nome = ?, cor = ? 
                    WHERE id = ? AND user_id = ?
                """, (nome, cor, id, user_id))
                
                conexao.commit()
                conexao.close()

                flash('Categoria atualizada com sucesso!', 'success')
                return redirect(url_for('categorias.listar_categorias'))

            except Exception as e:
                msg = f'Erro ao atualizar: {e}'

    return render_template(
        'pasta_categorias/crud/edit_categorias.html.jinja',
        categoria=categoria,
        msg=msg
    )