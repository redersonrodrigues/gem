"""
Logger Singleton para registrar operações críticas no banco de dados.
Os logs podem ser consultados pela interface administrativa.
"""
from threading import Lock
from datetime import datetime
from app.models.log import Log

class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls, db):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.db = db
            return cls._instance

    def log(self, user_id, action, details=None):
        """
        Registra uma operação crítica no banco de dados.
        Args:
            user_id (int): ID do usuário responsável pela ação.
            action (str): Descrição da ação (ex: 'create_medico').
            details (str, optional): Detalhes adicionais.
        """
        log_entry = Log(
            user_id=user_id,
            action=action,
            details=details,
            timestamp=datetime.utcnow()
        )
        self.db.add(log_entry)
        self.db.commit()

# Exemplo de uso:
# logger = Logger(db)
# logger.log(user_id=1, action='create_medico', details='Médico criado')
