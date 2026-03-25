def criar_tabela_tarefas(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tarefas'")

    if not cursor.fetchone():
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        categoria_id INTEGER,
        tarefa_sequencia INTEGER,
                       
        descricao TEXT NOT NULL,
        status TEXT DEFAULT 'pendente',
        prioridade TEXT DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta')),
                    
        data_inicio DATE,
        data_final DATE,
        data_finalizacao DATE,
                    
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
        FOREIGN KEY (user_id) REFERENCES cadastre_se(id) ON DELETE CASCADE,
        FOREIGN KEY(categoria_id) REFERENCES categorias_tarefas(id) ON DELETE SET NULL
        )
    """)
        print("✅ Tabela tarefas criada com sucesso!")

    else:
        # MODELO - ESTRUTURA
        cursor.execute("PRAGMA table_info(tarefas)")
        if not any(col[1] == 'ativo' for col in cursor.fetchall()):
            cursor.execute("ALTER TABLE tarefas ADD COLUMN ativo INTEGER DEFAULT 1")
            print("✅ Coluna ativo adicionada em tarefas!")

        cursor.execute("PRAGMA table_info(tarefas)")
        if not any(col[1] == 'excluido_em' for col in cursor.fetchall()):
            cursor.execute("ALTER TABLE tarefas ADD COLUMN excluido_em DATETIME")
            print("✅ Coluna excluido_em adicionada em tarefas!")
           
        cursor.execute("PRAGMA table_info(tarefas)")
        if not any(col[1] == 'excluido_por' for col in cursor.fetchall()):
            cursor.execute("ALTER TABLE tarefas ADD COLUMN excluido_por INTEGER")
            print("✅ Coluna excluido_por adicionada em tarefas!")

        print("ℹ️ Tabela tarefas já existe.")
