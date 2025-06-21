"""
Consulta: Cobertura de especialidades por turno (identificar lacunas).
Retorna especializações e turnos sem médicos escalados em determinado período.
"""
from sqlalchemy.orm import Session
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from datetime import date, timedelta


def cobertura_especialidades_por_turno(
    session: Session,
    data_inicio: date,
    data_fim: date
):
    """
    Retorna lista de tuplas (especializacao_id, nome_especializacao, data, turno) sem plantonista escalado.
    """
    especializacoes = session.query(Especializacao).all()
    dias = []
    atual = data_inicio
    while atual <= data_fim:
        dias.append(atual)
        atual = atual + timedelta(days=1)
    turnos = ["diurno", "noturno"]
    lacunas = []
    for esp in especializacoes:
        for dia in dias:
            for turno in turnos:
                plantao = session.query(EscalaPlantonista).filter(
                    EscalaPlantonista.data == dia,
                    EscalaPlantonista.turno == turno
                ).all()
                tem_esp = False
                for p in plantao:
                    # Verifica se algum dos médicos do plantão tem a especialização
                    if (p.medico1 and p.medico1.especializacao_id == esp.id) or \
                       (p.medico2 and p.medico2.especializacao_id == esp.id):
                        tem_esp = True
                        break
                if not tem_esp:
                    lacunas.append((esp.id, esp.nome, dia, turno))
    return lacunas
