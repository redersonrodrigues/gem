from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from datetime import date

def medicos_disponiveis_por_especializacao_periodo(db: Session, especializacao_id: int, data_inicio: date, data_fim: date):
    """
    Retorna médicos ativos de uma especialização que não estão escalados (plantão/sobreaviso) no período informado.
    """
    # Médicos ativos da especialização
    query_medicos = db.query(Medico).filter(
        Medico.status == "ativo",
        Medico.especializacao_id == especializacao_id
    )

    # Médicos escalados em plantão no período
    escalados_plantao = db.query(EscalaPlantonista.medico1_id).filter(
        EscalaPlantonista.data >= data_inicio,
        EscalaPlantonista.data <= data_fim
    )

    # Médicos escalados em sobreaviso no período
    escalados_sobreaviso = db.query(EscalaSobreaviso.medico1_id).filter(
        EscalaSobreaviso.data_inicial <= data_fim,
        EscalaSobreaviso.data_final >= data_inicio
    )

    # Excluir médicos escalados em qualquer escala no período
    query_medicos = query_medicos.filter(
        not_(Medico.id.in_(escalados_plantao)),
        not_(Medico.id.in_(escalados_sobreaviso))
    )

    return query_medicos.all()
