from werkzeug.security import generate_password_hash, check_password_hash

def criptografar_senha(senha):
    """GERA HASH SEGURO DA SENHA"""
    return generate_password_hash(senha)

def verificar_senha(senha_criptografada, senha_digitada):
    """VERIFICA SE A SENHA ESTÁ CORRETA"""
    return check_password_hash(senha_criptografada, senha_digitada)