from app.models.audit_log import AuditLog
from app.database import db
from datetime import datetime
from typing import Optional


class AuditService:
    @staticmethod
    def log_action(
        usuario: Optional[str],
        operacao: str,
        tabela: Optional[str],
        registro_id: Optional[int],
        dados_anteriores: Optional[str],
        dados_novos: Optional[str],
    ):
        log = AuditLog(
            usuario=usuario,
            data_hora=datetime.utcnow().isoformat(),
            operacao=operacao,
            tabela=tabela,
            registro_id=registro_id,
            dados_anteriores=dados_anteriores,
            dados_novos=dados_novos,
        )
        db.session.add(log)
        db.session.commit()

    @staticmethod
    def get_logs(limit: int = 100):
        return AuditLog.query.order_by(AuditLog.id.desc()).limit(limit).all()
