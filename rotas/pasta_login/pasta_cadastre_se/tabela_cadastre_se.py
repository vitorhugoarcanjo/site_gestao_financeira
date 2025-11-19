import sqlite3, os

caminho_banco = os.path.join(os.getcwd(), 'instance/banco_usuarios.db')

conexao_banco = sqlite3.connect(caminho_banco)

def cadastre_se_novo():

    cursor = conexao_banco.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cadastros_usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
            
    )
""")
    
    print('Tabela criada')
    conexao_banco.commit()
    conexao_banco.close()


cadastre_se_novo()