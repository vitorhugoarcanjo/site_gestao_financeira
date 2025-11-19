from flask import Flask, render_template

# LOGIN
from rotas.pasta_login.pasta_acesso_login.logica_login import bp_login

app = Flask(__name__)



# adicionar bluprints no app

# LOGIN
app.register_blueprint(bp_login, url_prefix="/login")


@app.route('/')
def appinicializar():
    return render_template('pasta_tela_inicial/paginainicial.html')

if __name__ == '__main__':
    app.run(debug=True)