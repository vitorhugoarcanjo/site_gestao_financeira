import sqlite3
import os

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

def migracao_correta():
    """Migração que renomeia colunas ANTIGAS para NOVOS nomes"""
    
    print(f"📂 Procurando banco em: {caminho_banco}")
    
    # 1. Primeiro verifica se o arquivo EXISTE
    if not os.path.exists(caminho_banco):
        print("❌ Banco não encontrado!")
        print("Crie o banco primeiro ou verifique o caminho.")
        return
    
    # 2. Agora sim, conecta ao banco
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    
    print("✅ Banco encontrado!")
    print("🔄 VERIFICANDO ESTRUTURA ATUAL...")
    
    # 3. Primeiro vejo quais colunas existem
    cursor.execute("PRAGMA table_info(transacoes)")
    colunas = cursor.fetchall()
    
    if not colunas:
        print("❌ Tabela 'transacoes' não existe!")
        conn.close()
        return
    
    colunas_existentes = [col[1] for col in colunas]
    print(f"Colunas encontradas: {colunas_existentes}")
    
    # 4. RENOMEAR colunas antigas (se existirem)
    print("\n🔧 RENOMEANDO COLUNAS...")
    
    renomeacoes = [
        ('data', 'data_emissao'),      # data → data_emissao
        ('valor', 'valor_total')       # valor → valor_total
    ]
    
    for antigo, novo in renomeacoes:
        if antigo in colunas_existentes:
            try:
                cursor.execute(f"ALTER TABLE transacoes RENAME COLUMN {antigo} TO {novo}")
                print(f"✅ {antigo} → {novo}")
            except Exception as e:
                print(f"⚠️  Não consegui renomear {antigo}: {e}")
    
    # 5. ADICIONAR colunas novas (se não existirem)
    print("\n➕ ADICIONANDO COLUNAS NOVAS...")
    
    colunas_novas = [
        ("data_vencimento", "DATE"),
        ("data_quitamento", "DATE"),
        ("data_alteracao", "DATE"),
        ("valor_parcela", "REAL"),
        ("numero_parcela", "INTEGER"),
        ("total_parcelas", "INTEGER")
    ]
    
    for nome, tipo in colunas_novas:
        if nome not in colunas_existentes:
            try:
                cursor.execute(f"ALTER TABLE transacoes ADD COLUMN {nome} {tipo}")
                print(f"✅ {nome} - Adicionada")
            except Exception as e:
                print(f"⚠️  {nome} - Erro: {e}")
        else:
            print(f"⏭️  {nome} - Já existe")
    
    # 6. ATUALIZAR dados (preencher campos novos)
    print("\n📝 ATUALIZANDO DADOS...")
    
    try:
        cursor.execute("""
            UPDATE transacoes 
            SET valor_parcela = valor_total,
                numero_parcela = 1,
                total_parcelas = 1,
                data_vencimento = data_emissao
            WHERE valor_parcela IS NULL
        """)
        print(f"✅ Atualizados {cursor.rowcount} registros")
    except Exception as e:
        print(f"⚠️  Erro ao atualizar: {e}")
    
    conn.commit()
    conn.close()
    print("\n🎉 MIGRAÇÃO FINALIZADA!")

# EXECUTAR
if __name__ == "__main__":
    migracao_correta()