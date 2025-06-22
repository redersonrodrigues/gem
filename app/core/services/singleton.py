"""
Padrão Singleton para serviços de cache local e logging estruturado.
Garante instância única e acesso global ao serviço.
"""
from threading import Lock

class CacheSingleton:
    _instance = None
    _lock = Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._cache = {}
            return cls._instance
    def get(self, key):
        return self._cache.get(key)
    def set(self, key, value):
        self._cache[key] = value
    def invalidate(self, key):
        if key in self._cache:
            del self._cache[key]

class LoggerSingleton:
    _instance = None
    _lock = Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._logs = []
            return cls._instance
    def log(self, message):
        self._logs.append(message)
    def get_logs(self):
        return list(self._logs)

# Exemplo de uso:
# cache = CacheSingleton()
# cache.set('chave', 'valor')
# valor = cache.get('chave')
# logger = LoggerSingleton()
# logger.log('Mensagem de log')
# logs = logger.get_logs()
