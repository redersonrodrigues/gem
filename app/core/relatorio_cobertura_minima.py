"""
Relatório: Cobertura mínima por especialidade (períodos críticos).
Gera consulta e exportação (CSV) das especialidades que não atingiram a cobertura mínima em determinado período.
"""
from sqlalchemy.orm import Session
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from datetime import date, timedelta
import csv
import io
from typing import List, Tuple

def relatorio_cobertura_minima(
    session: Session,
    data_inicio: date,
    data_fim: date,
    minimo_por_turno: int = 1
) -> List[Tuple[int, str, date, str]]:
    """
    Retorna lista de tuplas (especializacao_id, nome_especializacao, data, turno) onde a cobertura mínima não foi atingida.
    :param session: Sessão do banco de dados
    :param data_inicio: Data inicial do período
    :param data_fim: Data final do período
    :param minimo_por_turno: Quantidade mínima de médicos por especialidade e turno
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
                count_esp = 0
                for p in plantao:
                    if (p.medico1 and p.medico1.especializacao_id == esp.id):
                        count_esp += 1
                    if (p.medico2 and p.medico2.especializacao_id == esp.id):
                        count_esp += 1
                if count_esp < minimo_por_turno:
                    lacunas.append((esp.id, esp.nome, dia, turno, count_esp))
    return lacunas

def exportar_cobertura_minima_csv(lacunas: List[Tuple[int, str, date, str, int]]) -> str:
    """
    Exporta o relatório de cobertura mínima para CSV (string).
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID Especialização", "Especialização", "Data", "Turno", "Qtd Médicos"])
    for row in lacunas:
        writer.writerow(row)
    return output.getvalue()
