import os, sqlite3
from flask import Flask, request

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

def criar_parcelas(user_id, tipo, valor_total, descricao, categoria,
                    data_primeiro_vencimento, total_parcelas, intervalo_dias=30):
    from datetime import datetime, timedelta

    # 1º CONECTAR AO BANCO DE DADOS
    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    # 2º CALCULAR VALOR DE CADA PARCELA
    valor_parcela = valor_total / total_parcelas

    # 3º CONVERTER A DATA DE STRING PARA DATETIME
    # data_primeiro_vencimento vem como "2024-03-15"
    data_base = datetime.strptime(data_primeiro_vencimento, '%Y-%m-%d')

    # 4º DATA DE EMISSAO (HOJE)
    data_emissao = datetime.now().strftime('%Y-%m-%d')

    # 5º LOOP PARA CRIAR CADA PARCELA
    for numero in range(1, total_parcelas + 1):

        # CALCULAR DATA DE VENCIMENTO DESTA PARCELA
        dias_adicionais = (numero - 1) * intervalo_dias
        data_vencimento = data_base + timedelta(days=dias_adicionais)

        # inserir no banco de dados
        cursor.execute("""
            INSERT INTO transacoes
            (user_id, tipo, descricao, categoria, data_emissao, data_vencimento, valor_total, valor_parcela, numero_parcela, total_parcelas, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, tipo, descricao, categoria, data_emissao, data_vencimento.strftime('%Y-%m-%d'),
                valor_total, valor_parcela, numero, total_parcelas, 'aberto'))
        
    
    conexao_banco.commit()
    conexao_banco.close()

    print(f"✅ Criadas {total_parcelas} parcelas de R$ {valor_parcela:.2f}")