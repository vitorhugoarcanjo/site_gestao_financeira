import sqlite3
import os
from flask import request, session

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

class AuditoriaService:
    
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(caminho_banco)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def registrar(tarefa_id, acao, campo_alterado=None, valor_antigo=None, valor_novo=None):
        """Registra uma ação na auditoria"""
        try:
            conn = AuditoriaService.get_db_connection()
            cursor = conn.cursor()
            
            if valor_antigo and len(str(valor_antigo)) > 500:
                valor_antigo = str(valor_antigo)[:500] + "..."
            if valor_novo and len(str(valor_novo)) > 500:
                valor_novo = str(valor_novo)[:500] + "..."
            
            cursor.execute("""
                INSERT INTO tarefas_auditoria 
                (tarefa_id, acao, campo_alterado, valor_antigo, valor_novo, usuario_id, ip)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                tarefa_id,
                acao,
                campo_alterado,
                valor_antigo,
                valor_novo,
                session.get('user_id'),
                request.remote_addr
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao registrar auditoria: {e}")
            return False
    
    @staticmethod
    def listar_por_tarefa(tarefa_id, limite=50):
        """Lista todas as ações de uma tarefa"""
        try:
            conn = AuditoriaService.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ta.*, u.nome as usuario_nome
                FROM tarefas_auditoria ta
                LEFT JOIN cadastre_se u ON ta.usuario_id = u.id
                WHERE ta.tarefa_id = ?
                ORDER BY ta.data_hora DESC
                LIMIT ?
            """, (tarefa_id, limite))
            
            auditoria = cursor.fetchall()
            conn.close()
            return auditoria
        except Exception as e:
            print(f"Erro ao listar auditoria: {e}")
            return []