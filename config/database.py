from rotas.pasta_login.tabelas.cadastre_se import tabela_cadastre_se # TABELA DE CADASTRO DE USUÁRIO
from rotas.pasta_financas.tabelas.tabelas_gerais import tabela_categorias, tabela_transacoes # TABELA TRANSAÇÕES E CATEGORIAS
from rotas.pasta_tarefas.tabelas.tabela_tarefas import criar_tabela_tarefas # TABELA TAREFAS

def criar_todas_tabelas():
    tabela_cadastre_se()
    tabela_categorias()
    tabela_transacoes()
    criar_tabela_tarefas()

    print('Tabela criadas com sucesso!')