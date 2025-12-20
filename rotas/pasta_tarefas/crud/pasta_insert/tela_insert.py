from flask import Blueprint, request, render_template, session

bp_insert_tarefas = Blueprint('insert', __name__)

@bp_insert_tarefas.route('/', methods=['GET', 'POST'])
def iniinsert():
    if request.method == 'POST':
        user_id = session['user_id']
        descricao = request.form.get('descricao')
        status = request.form.get('status')
        data_inicio = request.form.get('data_inicio')
        data_final = request.form.get('data_final')


        return render_template('pasta_tarefas/crud/tela_insert.html')
    
    return render_template('pasta_tarefas/crud/tela_insert.html')