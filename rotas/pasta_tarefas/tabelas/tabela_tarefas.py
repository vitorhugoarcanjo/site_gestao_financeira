def criar_tabela_tarefas(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tarefas'")

    if not cursor.fetchone():
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        categoria_id INTEGER,
                       
        descricao TEXT NOT NULL,
        status TEXT DEFAULT 'pendente',
        prioridade TEXT DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta')),
                    
        data_inicio DATE,
        data_final DATE,
                    
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
        FOREIGN KEY (user_id) REFERENCES cadastre_se(id) ON DELETE CASCADE,
        FOREIGN KEY(categoria_id) REFERENCES categorias_tarefas(id) ON DELETE SET NULL
        )
    """)
        print("✅ Tabela tarefas criada com sucesso!")

    else:
        cursor.execute("PRAGMA table_info(tarefas)")
        if not any(col[1] == 'categoria_id' for col in cursor.fetchall()):
            cursor.execute("ALTER TABLE tarefas ADD COLUMN categoria_id INTEGER REFERENCES categorias_tarefas(id) ON DELETE SET NULL")
            print("✅ Coluna categoria_id adicionada em tarefas!")
        
        cursor.execute("PRAGMA table_info(tarefas)")
        if not any(col[1] == 'prioridade' for col in cursor.fetchall()):
            cursor.execute("ALTER TABLE tarefas ADD COLUMN prioridade TEXT")
            print("✅ Coluna prioridade adicionada em tarefas!")

        print("ℹ️ Tabela tarefas já existe.")
