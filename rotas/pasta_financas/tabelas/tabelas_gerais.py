import sqlite3, os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')


def tabela_transacoes():
    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        
        -- dados básicos da transação
        tipo TEXT,
        descricao TEXT,
        categoria TEXT,
        
        -- Datas importantes
        data_emissao DATE, -- Quando foi criada
        data_vencimento DATE,  -- Quando vence
        data_quitamento DATE,  -- Quando foi paga
        data_alteracao DATE,   -- Quando foi alterada
                   
        -- Valores
        valor_total REAL,      -- Valor total da compra
        valor_parcela REAL,    -- Valor desta parcela específica
                   
        -- Controle de parcelas(novo)
        numero_parcela INTEGER,  -- Ex: 1ª parcela
        total_parcelas INTEGER,  -- Ex: 10 parcelas no total
                   
        -- Status e controle
        status TEXT DEFAULT 'aberto',
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