"""
Consulta médicos inativos ou afastados em determinado período.
"""
from datetime import date
from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso


def medicos_inativos_afastados(
    session: Session, data_inicio: date, data_fim: date
):
    """
    Retorna médicos inativos OU afastados (sem escalas atribuídas) no período.
    - Inativo: status = 'inativo' no cadastro
    - Afastado: não possui escala de plantão ou sobreaviso no período
    """
    # Médicos inativos
    inativos = session.query(Medico).filter(
        Medico.status == 'inativo'
    ).all()

    # Médicos afastados (sem escalas no período)
    subq_plantao = session.query(EscalaPlantonista.medico1_id).filter(
        EscalaPlantonista.data >= data_inicio,
        EscalaPlantonista.data <= data_fim
    )
    subq_sobreaviso = session.query(EscalaSobreaviso.medico1_id).filter(
        EscalaSobreaviso.data_inicial <= data_fim,
        EscalaSobreaviso.data_final >= data_inicio
    )
    afastados = session.query(Medico).filter(
        Medico.status == 'ativo',
        ~Medico.id.in_(subq_plantao),
        ~Medico.id.in_(subq_sobreaviso)
    ).all()

    return {
        'inativos': inativos,
        'afastados': afastados
    }
