import os, sqlite3

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

def criar_tabela_tarefas():
    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
                   
    descricao TEXT NOT NULL,
    status TEXT DEFAULT 'pendente',
                   
    data_inicio DATE,
    data_final DATE,
                   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   
    FOREIGN KEY (user_id) REFERENCES cadastre_se(id) ON DELETE CASCADE
    )
""")

    conexao_banco.commit()
    conexao_banco.close()
