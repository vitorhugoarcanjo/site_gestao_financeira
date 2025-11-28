# migration_status.py
import sqlite3
import os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

def add_coluna_status():
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    
    try:
        # Tenta adicionar a coluna
        cursor.execute('ALTER TABLE transacoes ADD COLUMN status TEXT DEFAULT "aberto"')
        conn.commit()
        print("✅ Coluna status adicionada com sucesso!")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✅ Coluna status já existe!")
        else:
            print(f"❌ Erro: {e}")
    
    conn.close()

if __name__ == '__main__':
    add_coluna_status()