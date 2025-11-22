from flask import Flask, render_template
import os


# CADASTRE-SE
from rotas.pasta_login.tabelas.cadastre_se import tabela_cadastre_se
from rotas.pasta_login.pasta_cadastre_se.tela_cadastre_se import bp_cadastre_se

# LOGIN
from rotas.pasta_login.pasta_acesso_login.logica_login import bp_login

app = Flask(__name__)


app.secret_key = os.urandom(24)




# ---------------- ADICIONAR BLUEPRINTS ----------------------- #
# CADASTRE_SE
app.register_blueprint(bp_cadastre_se, url_prefix="/cadastre_se")

# LOGIN
app.register_blueprint(bp_login, url_prefix="/login")




@app.route('/')
def appinicializar():
    return render_template('pasta_tela_inicial/paginainicial.html')

# INICIALIZA O APP
if __name__ == '__main__':
    tabela_cadastre_se()
    app.run(debug=True)