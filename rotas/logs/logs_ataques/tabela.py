def tabela_ataque(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs_ataques (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip VARCHAR(45),
        rota VARCHAR(255),
        metodo VARCHAR(10),
        user_agent TEXT,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        padrao_detectado VARCHAR(100)
    );
""")