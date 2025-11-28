from flask import Flask, render_template
import os
from dotenv import load_dotenv

# CRIAÇÃO DE TABELAS
from config.database import criar_todas_tabelas


# CADASTRE-SE
from rotas.pasta_login.pasta_cadastre_se.tela_cadastre_se import bp_cadastre_se

# LOGIN
from rotas.pasta_login.pasta_acesso_login.logica_login import bp_login

# TELA POS LOGIN
from rotas.pasta_tela_pos_login.tela_pos_login import bp_pos_login

# PASTA FINANÇAS
from rotas.pasta_financas.financas import bp_financas
from rotas.pasta_financas.crud.insert_transacao import bp_insert_transacao
from rotas.pasta_financas.crud.edit_transacao import bp_edit_transacao
from rotas.pasta_financas.crud.delete_transacao import bp_delete

# PASTA DASHBOARD
from rotas.pasta_dashboard.dashboard import bp_dashboard

# PASTA CONFIGURACOES
from rotas.pasta_config.config import bp_config

load_dotenv()

app = Flask(__name__)


app.secret_key = os.getenv('SECRET_KEY')




# ----------------- ADICIONAR BLUEPRINTS ----------------------- #
# CADASTRE_SE
app.register_blueprint(bp_cadastre_se, url_prefix="/cadastre_se")

# LOGIN
app.register_blueprint(bp_login, url_prefix="/login")

# POS LOGIN
app.register_blueprint(bp_pos_login, url_prefix="/pos_login")

# FINANÇAS
app.register_blueprint(bp_financas, url_prefix="/financas")
app.register_blueprint(bp_insert_transacao, url_prefix='/nova_transacao')
app.register_blueprint(bp_edit_transacao, url_prefix="/edit_transacoes")
app.register_blueprint(bp_delete, url_prefix='/deletar_transacao')

# DASHBOARD
app.register_blueprint(bp_dashboard, url_prefix="/dashboard")

# CONFIGURACOES
app.register_blueprint(bp_config, url_prefix="/config")


@app.route('/')
def appinicializar():
    return render_template('pasta_tela_inicial/paginainicial.html')

# INICIALIZA O APP
if __name__ == '__main__':
    criar_todas_tabelas()
    app.run(debug=True)