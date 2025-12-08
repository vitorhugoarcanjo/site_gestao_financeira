# utils/versao_nova_cache.py
import time

def get_static_version():
    """Retorna versão que muda a cada hora"""
    return str(int(time.time() / 3600))

# Ou se quiser constante também
CSS_VERSION = get_static_version()