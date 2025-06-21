"""
Consulta o histórico de alterações (auditoria) de uma escala (plantonista ou sobreaviso).
"""
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from typing import List, Optional
from datetime import datetime

def consultar_historico_escalas(db: Session, escala_id: int, tipo: str, data_inicio: Optional[datetime]=None, data_fim: Optional[datetime]=None) -> List[dict]:
    """
    Retorna o histórico de alterações de uma escala específica.
    :param db: Sessão do banco de dados
    :param escala_id: ID da escala
    :param tipo: 'plantonista' ou 'sobreaviso'
    :param data_inicio: Data inicial do filtro (opcional)
    :param data_fim: Data final do filtro (opcional)
    :return: Lista de dicionários com informações da auditoria
    """
    if tipo == 'plantonista':
        entity = EscalaPlantonista
    elif tipo == 'sobreaviso':
        entity = EscalaSobreaviso
    else:
        raise ValueError('Tipo de escala inválido')

    query = db.query(AuditLog).filter(
        AuditLog.tabela == entity.__tablename__,
        AuditLog.registro_id == escala_id
    )
    if data_inicio:
        query = query.filter(AuditLog.data_hora >= data_inicio.isoformat())
    if data_fim:
        query = query.filter(AuditLog.data_hora <= data_fim.isoformat())
    query = query.order_by(AuditLog.data_hora.desc())
    return [
        {
            'acao': log.operacao,
            'usuario': log.usuario,
            'data': log.data_hora,
            'alteracoes': log.dados_novos  # ou log.dados_anteriores, conforme necessidade
        }
        for log in query.all()
    ]
