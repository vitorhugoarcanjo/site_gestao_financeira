from rotas.pasta_login.tabelas.cadastre_se import tabela_cadastre_se
from rotas.pasta_financas.tabelas.tabelas_gerais import tabela_categorias, tabela_transacoes

def criar_todas_tabelas():
    tabela_cadastre_se()
    tabela_categorias()
    tabela_transacoes()

    print('Tabela criadas com sucesso!')