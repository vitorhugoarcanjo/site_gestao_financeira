def tabela_cadastre_se(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cadastre_se(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT 1
                   
    )
""")
