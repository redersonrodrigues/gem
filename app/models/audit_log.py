from sqlalchemy import Column, Integer, String, Text
from .base import Base

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String)
    data_hora = Column(String)  # ISO datetime string
    operacao = Column(String)
    tabela = Column(String)
    registro_id = Column(Integer)
    dados_anteriores = Column(Text)
    dados_novos = Column(Text)

    def __repr__(self):
        return f"<AuditLog(usuario={self.usuario}, operacao={self.operacao}, tabela={self.tabela}, registro_id={self.registro_id})>"
