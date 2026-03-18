""" ARQUIVO PRINCIPAL """
import os
from datetime import timedelta # TEMPO DE LOGIN
from flask import Flask, render_template
from dotenv import load_dotenv # CHAVE SECRETA

from config.database import criar_todas_tabelas, organizar_tarefa_sequencia # CRIAÇÃO DE TABELAS
from config.imports_rotas import logica_imports # IMPORTS DE BLUEPRINTS


load_dotenv()

app = Flask(__name__)
logica_imports(app)

app.secret_key = os.getenv('SECRET_KEY')

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


@app.route('/')
def ini_app():
    """ INICIO DO MEU APP """
    return render_template('pasta_tela_inicial/paginainicial.html')

# INICIALIZA O APP
if __name__ == '__main__':
    criar_todas_tabelas()
    organizar_tarefa_sequencia()
    app.run(debug=True)
