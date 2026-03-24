def tabela_categorias_tarefas(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categorias_tarefas'")

    if not cursor.fetchone():
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias_tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,              
        nome TEXT NOT NULL,              
        cor TEXT DEFAULT '#CCCCCC',
        FOREIGN KEY(user_id) REFERENCES cadastre_se(id) ON DELETE CASCADE,
        UNIQUE(user_id, nome)                             
        )
    """)
        print("✅ Tabela categorias_tarefas criada com sucesso!")

    else:
        print("ℹ️ Tabela categorias_tarefas já existe.")
