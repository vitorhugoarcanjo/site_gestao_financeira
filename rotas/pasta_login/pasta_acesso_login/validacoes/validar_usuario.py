import sqlite3
from rotas.pasta_login.pasta_cadastre_se.validacoes.criptografia_snh import verificar_senha

def validar_usuario_bd(caminho_banco, nome_ou_email, senha):

    conexao_banco = sqlite3.connect(caminho_banco)
    cursor = conexao_banco.cursor()

    cursor.execute('SELECT nome, senha FROM cadastre_se WHERE (nome = ? OR email = ?)', (nome_ou_email, nome_ou_email))
    usuario = cursor.fetchone()



    conexao_banco.close()


    if usuario and verificar_senha(usuario[1], senha):  # ← VERIFICA SENHA CRIPTOGRAFADA

        return True
    else:
        return False

    
