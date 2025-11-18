from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def appinicializar():
    return render_template('pasta_tela_inicial/paginainicial.html')

if __name__ == '__main__':
    app.run(debug=True)