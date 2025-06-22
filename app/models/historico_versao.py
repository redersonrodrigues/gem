from sqlalchemy import Column, Integer, String, DateTime, Text
from .base import Base
from datetime import datetime

class HistoricoVersao(Base):
    """
    Modelo para versionamento de dados e rastreamento de alterações em registros.
    Cada alteração relevante em um registro gera uma nova versão neste histórico.
    """
    __tablename__ = 'historico_versao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tabela = Column(String, nullable=False)
    registro_id = Column(Integer, nullable=False)
    versao = Column(Integer, nullable=False)
    usuario = Column(String)
    data_hora = Column(DateTime, default=datetime.utcnow)
    dados = Column(Text)  # JSON serializado do estado do registro

    def __repr__(self):
        return f"<HistoricoVersao(tabela={self.tabela}, registro_id={self.registro_id}, versao={self.versao})>"
