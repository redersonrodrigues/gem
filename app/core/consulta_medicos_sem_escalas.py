"""
Consulta: Médicos sem escalas atribuídas em um intervalo de datas.
Retorna lista de médicos ativos que não possuem plantão nem sobreaviso no período informado.
"""
from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from datetime import date


def medicos_sem_escalas(
    session: Session,
    data_inicio: date,
    data_fim: date,
    especializacao_id=None
):
    """
    Retorna médicos ativos sem plantão ou sobreaviso no período.
    """
    subq_plantao = session.query(EscalaPlantonista.medico1_id).filter(
        EscalaPlantonista.data >= data_inicio,
        EscalaPlantonista.data <= data_fim
    )
    subq_sobreaviso = session.query(EscalaSobreaviso.medico1_id).filter(
        EscalaSobreaviso.data_inicial <= data_fim,
        EscalaSobreaviso.data_final >= data_inicio
    )
    query = session.query(Medico).filter(
        Medico.status == "ativo",
        ~Medico.id.in_(subq_plantao),
        ~Medico.id.in_(subq_sobreaviso)
    )
    if especializacao_id:
        query = query.filter(Medico.especializacao_id == especializacao_id)
    return query.all()
