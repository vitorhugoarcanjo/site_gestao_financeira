def tabela_auditoria_tarefas(cursor):

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tarefas_auditoria'")

    if not cursor.fetchone():    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas_auditoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarefa_id INTEGER,
        acao VARCHAR(50),  -- 'criada', 'editada', 'concluida', 'excluida', 'restaurada'
        campo_alterado VARCHAR(100),
        valor_antigo TEXT,
        valor_novo TEXT,
        usuario_id INTEGER,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        ip VARCHAR(45),
        FOREIGN KEY (tarefa_id) REFERENCES tarefas(id),
        FOREIGN KEY (usuario_id) REFERENCES cadastre_se(id)
        )
    """)
        print(f"Tabela {cursor} criada com sucesso!")

    else:
        print("Tabela já está criada!")