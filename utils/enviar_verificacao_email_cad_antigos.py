# scripts/enviar_verificacao_antigos.py
import sqlite3
import os
import sys

# Adiciona o caminho do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rotas.pasta_login.pasta_cadastre_se.autenticador_email.email_utils import gerar_codigo, enviar_email_confirmacao, salvar_codigo_verificacao

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

def main():
    print("🚀 Iniciando envio de verificação para usuários antigos...")
    
    with sqlite3.connect(caminho_banco) as conn:
        cursor = conn.cursor()
        
        # Busca usuários que ainda não verificaram email
        cursor.execute("SELECT id, email, nome FROM cadastre_se WHERE email_verificado = 0 AND ativo = 1")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("✅ Todos os usuários já verificaram o email!")
            return
        
        print(f"📧 Enviando emails para {len(usuarios)} usuários...")
        print("-" * 50)
        
        enviados = 0
        erros = 0
        
        for user_id, email, nome in usuarios:
            codigo = gerar_codigo()
            sucesso, mensagem = enviar_email_confirmacao(email, codigo)
            
            if sucesso:
                salvar_codigo_verificacao(user_id, codigo)
                print(f"✅ Enviado para {nome} ({email})")
                enviados += 1
            else:
                print(f"❌ Erro para {nome} ({email}): {mensagem}")
                erros += 1
        
        print("-" * 50)
        print(f"📊 Resumo: {enviados} enviados, {erros} erros")

if __name__ == "__main__":
    main()