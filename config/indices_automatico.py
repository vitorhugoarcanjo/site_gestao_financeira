import sqlite3
import os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

def criar_indices(cursor):
    """Cria índices para otimizar consultas"""
    
    print("📊 Criando índices...")
    
    # ============================================
    # TAREFAS
    # ============================================
    print("  📋 Índices de tarefas...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tarefas_user_id ON tarefas(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tarefas_status ON tarefas(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tarefas_prioridade ON tarefas(prioridade)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tarefas_data_inicio ON tarefas(data_inicio)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tarefas_data_final ON tarefas(data_final)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tarefas_user_status ON tarefas(user_id, status)")
    
    # ============================================
    # TRANSAÇÕES (FINANÇAS)
    # ============================================
    print("  💰 Índices de transações...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacoes_user_id ON transacoes(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacoes_tipo ON transacoes(tipo)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacoes_status ON transacoes(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacoes_data_emissao ON transacoes(data_emissao)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacoes_data_vencimento ON transacoes(data_vencimento)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacoes_user_tipo ON transacoes(user_id, tipo)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacoes_user_status ON transacoes(user_id, status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transacoes_user_data_emissao ON transacoes(user_id, data_emissao)")
    
    # ============================================
    # CATEGORIAS
    # ============================================
    print("  🏷️ Índices de categorias...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_categorias_tarefas_user_id ON categorias_tarefas(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_categorias_financas_user_id ON categorias_financas(user_id)")
    
    # ============================================
    # LOGS
    # ============================================
    print("  📝 Índices de logs...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_acesso_user_id ON logs_acesso(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_acesso_data_hora ON logs_acesso(data_hora)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_acesso_rota ON logs_acesso(rota)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_erros_user_id ON logs_erros(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_erros_data_hora ON logs_erros(data_hora)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_ataques_ip ON logs_ataques(ip)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_ataques_data_hora ON logs_ataques(data_hora)")
    
    print("✅ Índices criados/verificados com sucesso!")

def criar_todos_indices():
    """Função para criar todos os índices"""
    print("🚀 Iniciando criação de índices...")
    print(f"📁 Banco de dados: {caminho_banco}")
    
    if not os.path.exists(caminho_banco):
        print(f"❌ Banco de dados não encontrado em: {caminho_banco}")
        return
    
    try:
        conn = sqlite3.connect(caminho_banco)
        cursor = conn.cursor()
        
        criar_indices(cursor)
        conn.commit()
        
        print("\n🎉 Todos os índices foram criados/verificados com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar índices: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    criar_todos_indices()