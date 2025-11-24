import sqlite3, os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')


def tabela_transacoes():
    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    tipo TEXT,
    valor REAL,
    descricao TEXT,
    categoria TEXT,
    data DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES cadastre_se(id) ON DELETE CASCADE
                   
    )
""")
    
    conexao_banco.commit()
    conexao_banco.close()


def tabela_categorias():
    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    nome TEXT,
    tipo TEXT,               
    cor TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES cadastre_se(id) ON DELETE CASCADE
    )
""")
    
    conexao_banco.commit()
    conexao_banco.close()