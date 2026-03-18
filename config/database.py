import os
import sqlite3
caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')


from rotas.pasta_login.tabelas.cadastre_se import tabela_cadastre_se # TABELA DE CADASTRO DE USUÁRIO

from rotas.pasta_financas.tabelas.tabelas_gerais import tabela_transacoes # TABELA TRANSAÇÕES E CATEGORIAS
from rotas.pasta_categorias.categorias_financas.tabela.tabela_categoria_financas import tabela_categorias_financas # TABELA CATEGORIA FINANCAS

from rotas.pasta_tarefas.tabelas.tabela_tarefas import criar_tabela_tarefas # TABELA TAREFAS
from rotas.pasta_categorias.categorias_tarefas.tabela.tabela_categoria_tarefas import tabela_categorias_tarefas # TABELA CATEGORIA_TAREFAS

def criar_todas_tabelas():
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    tabela_cadastre_se(cursor)

    # FINANÇAS
    tabela_categorias_financas(cursor)
    tabela_transacoes(cursor)

    # TAREFAS
    criar_tabela_tarefas(cursor)
    tabela_categorias_tarefas(cursor)


    print('Tabela criadas com sucesso!')
    conexao.commit()
    conexao.close()


def organizar_tarefa_sequencia():
    with sqlite3.connect(caminho_banco) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT user_id FROM tarefas ORDER BY user_id")
        users = cursor.fetchall()
        
        for user_row in users:
            user_id = user_row[0]
            cursor.execute("SELECT id FROM tarefas WHERE user_id = ? ORDER BY created_at ASC", (user_id,))
            tarefas_user = cursor.fetchall()
            
            for seq, tarefa_id in enumerate(tarefas_user, 1):
                cursor.execute("UPDATE tarefas SET tarefa_sequencia = ? WHERE id = ?", (seq, tarefa_id[0]))
        
        conn.commit()
        print("✅ tarefa_sequencia preenchida!")
