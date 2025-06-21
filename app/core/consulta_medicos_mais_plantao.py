"""
Consulta: Médicos com maior número de plantões em determinado período.
Retorna lista de médicos ordenada pelo total de plantões no intervalo informado.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.medico import Medico
from app.models.escala_plantonista import EscalaPlantonista
from datetime import date


def medicos_mais_plantao(
    session: Session,
    data_inicio: date,
    data_fim: date,
    especializacao_id=None
):
    """
    Retorna médicos ordenados pelo número de plantões no período.
    """
    query = (
        session.query(
            Medico.id,
            Medico.nome,
            func.count(EscalaPlantonista.id).label('total_plantao')
        )
        .join(EscalaPlantonista, EscalaPlantonista.medico1_id == Medico.id)
        .filter(
            EscalaPlantonista.data >= data_inicio,
            EscalaPlantonista.data <= data_fim
        )
    )
    if especializacao_id:
        query = query.filter(Medico.especializacao_id == especializacao_id)
    query = query.group_by(Medico.id, Medico.nome)
    query = query.order_by(func.count(EscalaPlantonista.id).desc())
    return query.all()
