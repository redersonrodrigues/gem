"""
Consulta escalas com conflitos de horário ou sobreposição de médicos.
"""
from datetime import date
from sqlalchemy.orm import Session
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico

def escalas_com_conflitos(
    session: Session, data_inicio: date, data_fim: date
):
    """
    Retorna lista de conflitos de escalas:
    - Plantões ou sobreavisos do mesmo médico que se sobrepõem em data/turno.
    - Plantão e sobreaviso do mesmo médico no mesmo período.
    """
    conflitos = []
    # Busca todos os plantões e sobreavisos no período
    plantao = session.query(EscalaPlantonista).filter(
        EscalaPlantonista.data >= data_inicio,
        EscalaPlantonista.data <= data_fim
    ).all()
    sobreaviso = session.query(EscalaSobreaviso).filter(
        EscalaSobreaviso.data_inicial <= data_fim,
        EscalaSobreaviso.data_final >= data_inicio
    ).all()
    # Indexa por médico
    por_medico = {}
    for p in plantao:
        por_medico.setdefault(p.medico1_id, []).append(('plantao', p))
    for s in sobreaviso:
        por_medico.setdefault(s.medico1_id, []).append(('sobreaviso', s))
    # Verifica sobreposição para cada médico
    for medico_id, escalas in por_medico.items():
        for i in range(len(escalas)):
            tipo_i, esc_i = escalas[i]
            for j in range(i+1, len(escalas)):
                tipo_j, esc_j = escalas[j]
                # Plantão x Plantão: mesmo dia e turno
                if tipo_i == tipo_j == 'plantao':
                    if esc_i.data == esc_j.data and esc_i.turno == esc_j.turno:
                        conflitos.append({
                            'medico_id': medico_id,
                            'tipo': 'plantao-plantao',
                            'data': esc_i.data,
                            'turno': esc_i.turno
                        })
                # Sobreaviso x Sobreaviso: interseção de datas
                if tipo_i == tipo_j == 'sobreaviso':
                    if not (
                        esc_i.data_final < esc_j.data_inicial or
                        esc_j.data_final < esc_i.data_inicial
                    ):
                        conflitos.append({
                            'medico_id': medico_id,
                            'tipo': 'sobreaviso-sobreaviso',
                            'data_inicial': max(
                                esc_i.data_inicial, esc_j.data_inicial
                            ),
                            'data_final': min(
                                esc_i.data_final, esc_j.data_final
                            )
                        })
                # Plantão x Sobreaviso: plantão dentro do período de sobreaviso
                if (tipo_i, tipo_j) in [
                    ('plantao', 'sobreaviso'),
                    ('sobreaviso', 'plantao')
                ]:
                    plantao_esc = esc_i if tipo_i == 'plantao' else esc_j
                    sobreaviso_esc = esc_j if tipo_i == 'plantao' else esc_i
                    if (
                        sobreaviso_esc.data_inicial <= plantao_esc.data and
                        plantao_esc.data <= sobreaviso_esc.data_final
                    ):
                        conflitos.append({
                            'medico_id': medico_id,
                            'tipo': 'plantao-sobreaviso',
                            'data': plantao_esc.data,
                            'turno': plantao_esc.turno
                        })
    return conflitos
