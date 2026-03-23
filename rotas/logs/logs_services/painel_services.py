# rotas/logs/services.py
import os
import sqlite3
import time
import traceback
from datetime import datetime
from flask import request, session
import json

caminho_banco = os.path.join(os.getcwd(), 'instance', 'banco_de_dados.db')

class LogService:
    """Serviço para gerenciar logs do sistema"""
    
    @staticmethod
    def get_db_connection():
        """Retorna conexão com o banco"""
        conn = sqlite3.connect(caminho_banco)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def registrar_erro(mensagem, arquivo=None, linha=None, stack_trace=None):
        """Registra um erro no banco"""
        try:
            conn = LogService.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO logs_erro (mensagem, arquivo, linha, usuario_id, rota, metodo, stack_trace)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                mensagem[:500],  # Limita tamanho
                arquivo,
                linha,
                session.get('usuario_id'),
                request.path if request else None,
                request.method if request else None,
                stack_trace[:1000] if stack_trace else None
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao registrar log de erro: {e}")
            return False
    
    @staticmethod
    def registrar_acesso(usuario_id, ip, user_agent, rota, metodo, status_code, tempo_resposta):
        """Registra um acesso no banco"""
        try:
            conn = LogService.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO logs_acesso (usuario_id, ip, user_agent, rota, metodo, status_code, tempo_resposta)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                usuario_id,
                ip[:45],
                user_agent[:500] if user_agent else None,
                rota[:255],
                metodo[:10],
                status_code,
                tempo_resposta
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao registrar log de acesso: {e}")
            return False
    
    @staticmethod
    def registrar_acao(usuario_id, acao, tabela_afetada, registro_id, dados_antes=None, dados_depois=None):
        """Registra uma ação do usuário"""
        try:
            conn = LogService.get_db_connection()
            cursor = conn.cursor()
            
            # Converte dicionários para JSON
            dados_antes_json = json.dumps(dados_antes) if dados_antes else None
            dados_depois_json = json.dumps(dados_depois) if dados_depois else None
            
            cursor.execute("""
                INSERT INTO logs_acao (usuario_id, acao, tabela_afetada, registro_id, dados_antes, dados_depois, ip)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                usuario_id,
                acao[:100],
                tabela_afetada[:50],
                registro_id,
                dados_antes_json,
                dados_depois_json,
                request.remote_addr if request else None
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao registrar log de ação: {e}")
            return False
    
    @staticmethod
    def listar_erros(limite=100, offset=0, filtro=None):
        """Lista erros com paginação e filtro"""
        try:
            conn = LogService.get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM logs_erro"
            params = []
            
            if filtro:
                query += " WHERE mensagem LIKE ?"
                params.append(f"%{filtro}%")
            
            query += " ORDER BY data_hora DESC LIMIT ? OFFSET ?"
            params.extend([limite, offset])
            
            cursor.execute(query, params)
            erros = cursor.fetchall()
            
            # Total
            cursor.execute("SELECT COUNT(*) as total FROM logs_erro")
            total = cursor.fetchone()['total']
            
            conn.close()
            return {'dados': erros, 'total': total}
        except Exception as e:
            print(f"Erro ao listar erros: {e}")
            return {'dados': [], 'total': 0}
    
    @staticmethod
    def listar_acessos(limite=100, offset=0, filtro=None):
        """Lista acessos com paginação e filtro"""
        try:
            conn = LogService.get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT la.*, u.nome as usuario_nome 
                FROM logs_acesso la
                LEFT JOIN usuarios u ON la.usuario_id = u.id
            """
            params = []
            
            if filtro:
                query += " WHERE la.rota LIKE ? OR u.nome LIKE ?"
                params.append(f"%{filtro}%")
                params.append(f"%{filtro}%")
            
            query += " ORDER BY la.data_hora DESC LIMIT ? OFFSET ?"
            params.extend([limite, offset])
            
            cursor.execute(query, params)
            acessos = cursor.fetchall()
            
            # Total
            cursor.execute("SELECT COUNT(*) as total FROM logs_acesso")
            total = cursor.fetchone()['total']
            
            conn.close()
            return {'dados': acessos, 'total': total}
        except Exception as e:
            print(f"Erro ao listar acessos: {e}")
            return {'dados': [], 'total': 0}
    
    @staticmethod
    def obter_erro_por_id(erro_id):
        """Obtém detalhes de um erro específico"""
        try:
            conn = LogService.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT le.*, u.nome as usuario_nome 
                FROM logs_erro le
                LEFT JOIN usuarios u ON le.usuario_id = u.id
                WHERE le.id = ?
            """, (erro_id,))
            
            erro = cursor.fetchone()
            conn.close()
            return erro
        except Exception as e:
            print(f"Erro ao obter erro: {e}")
            return None
    
    @staticmethod
    def obter_acesso_por_id(acesso_id):
        """Obtém detalhes de um acesso específico"""
        try:
            conn = LogService.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT la.*, u.nome as usuario_nome 
                FROM logs_acesso la
                LEFT JOIN usuarios u ON la.usuario_id = u.id
                WHERE la.id = ?
            """, (acesso_id,))
            
            acesso = cursor.fetchone()
            conn.close()
            return acesso
        except Exception as e:
            print(f"Erro ao obter acesso: {e}")
            return None
    
    @staticmethod
    def estatisticas():
        """Retorna estatísticas dos logs"""
        try:
            conn = LogService.get_db_connection()
            cursor = conn.cursor()
            
            # Total de erros
            cursor.execute("SELECT COUNT(*) as total FROM logs_erro")
            total_erros = cursor.fetchone()['total']
            
            # Total de acessos
            cursor.execute("SELECT COUNT(*) as total FROM logs_acesso")
            total_acessos = cursor.fetchone()['total']
            
            # Erros dos últimos 7 dias
            cursor.execute("""
                SELECT COUNT(*) as total FROM logs_erro 
                WHERE data_hora >= date('now', '-7 days')
            """)
            erros_7dias = cursor.fetchone()['total']
            
            # Acessos dos últimos 7 dias
            cursor.execute("""
                SELECT COUNT(*) as total FROM logs_acesso 
                WHERE data_hora >= date('now', '-7 days')
            """)
            acessos_7dias = cursor.fetchone()['total']
            
            conn.close()
            
            return {
                'total_erros': total_erros,
                'total_acessos': total_acessos,
                'erros_7dias': erros_7dias,
                'acessos_7dias': acessos_7dias
            }
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {
                'total_erros': 0,
                'total_acessos': 0,
                'erros_7dias': 0,
                'acessos_7dias': 0
            }