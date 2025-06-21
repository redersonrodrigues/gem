from sqlalchemy.orm import Session
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from datetime import date
from typing import Optional, List, Dict

def consultar_escalas_mes(
    db: Session,
    ano: int,
    mes: int,
    especializacao_id: Optional[int] = None,
    medico_id: Optional[int] = None
) -> Dict[str, List]:
    """
    Consulta todas as escalas de plantão e sobreaviso de um mês, podendo filtrar por especialização e/ou médico.
    Retorna um dicionário com listas de plantões e sobreavisos.
    """
    data_inicio = date(ano, mes, 1)
    if mes == 12:
        data_fim = date(ano + 1, 1, 1)
    else:
        data_fim = date(ano, mes + 1, 1)

    # Plantões
    query_plantao = db.query(EscalaPlantonista).filter(
        EscalaPlantonista.data >= data_inicio,
        EscalaPlantonista.data < data_fim
    )
    if especializacao_id:
        query_plantao = query_plantao.join(Medico, EscalaPlantonista.medico1_id == Medico.id)
        query_plantao = query_plantao.filter(Medico.especializacao_id == especializacao_id)
    if medico_id:
        query_plantao = query_plantao.filter(
            (EscalaPlantonista.medico1_id == medico_id) |
            (EscalaPlantonista.medico2_id == medico_id)
        )
    plantao_result = query_plantao.all()

    # Sobreaviso
    query_sobreaviso = db.query(EscalaSobreaviso).filter(
        EscalaSobreaviso.data_inicial < data_fim,
        EscalaSobreaviso.data_final >= data_inicio
    )
    if especializacao_id:
        query_sobreaviso = query_sobreaviso.filter(EscalaSobreaviso.especializacao_id == especializacao_id)
    if medico_id:
        query_sobreaviso = query_sobreaviso.filter(EscalaSobreaviso.medico1_id == medico_id)
    sobreaviso_result = query_sobreaviso.all()

    return {
        "plantao": plantao_result,
        "sobreaviso": sobreaviso_result
    }
