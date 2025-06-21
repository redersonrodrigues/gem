from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime
import hashlib

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(128), nullable=False)
    perfil = Column(String(20), nullable=False, default='usuario')  # admin, usuario, etc
    status = Column(Boolean, default=True)  # ativo/inativo
    data_criacao = Column(DateTime, default=datetime.utcnow)

    def set_senha(self, senha: str):
        self.senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def verificar_senha(self, senha: str) -> bool:
        return self.senha_hash == hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def is_admin(self) -> bool:
        return self.perfil == 'admin'

    def is_active(self) -> bool:
        return self.status is True

    def __repr__(self):
        return (
            f"<Usuario(nome={self.nome}, login={self.login}, "
            f"perfil={self.perfil}, status={self.status})>"
        )
