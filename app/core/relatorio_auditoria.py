"""
Relatório de auditoria de alterações em escalas, médicos e especializações.
Gera consulta e exportação (CSV/PDF) do log de auditoria.
"""
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from typing import List, Optional
from datetime import datetime
import csv
import io


def consultar_auditoria(
    db: Session,
    tabela: Optional[str] = None,
    usuario: Optional[str] = None,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
) -> List[dict]:
    """
    Consulta o log de auditoria filtrando por tabela, usuário e período.
    :param db: Sessão do banco de dados
    :param tabela: Nome da tabela ('medicos', 'especializacoes', 'escalas_plantonistas', 'escalas_sobreaviso')
    :param usuario: Nome do usuário (opcional)
    :param data_inicio: Data inicial do filtro (opcional)
    :param data_fim: Data final do filtro (opcional)
    :return: Lista de dicionários com informações da auditoria
    """
    query = db.query(AuditLog)
    if tabela:
        query = query.filter(AuditLog.tabela == tabela)
    if usuario:
        query = query.filter(AuditLog.usuario == usuario)
    if data_inicio:
        query = query.filter(AuditLog.data_hora >= data_inicio.isoformat())
    if data_fim:
        query = query.filter(AuditLog.data_hora <= data_fim.isoformat())
    query = query.order_by(AuditLog.data_hora.desc())
    return [
        {
            'id': log.id,
            'usuario': log.usuario,
            'data_hora': log.data_hora,
            'operacao': log.operacao,
            'tabela': log.tabela,
            'registro_id': log.registro_id,
            'dados_anteriores': log.dados_anteriores,
            'dados_novos': log.dados_novos,
        }
        for log in query.all()
    ]

def exportar_auditoria_csv(auditoria: List[dict]) -> str:
    """
    Exporta o relatório de auditoria para CSV (string).
    """
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            'id', 'usuario', 'data_hora', 'operacao', 'tabela', 'registro_id', 'dados_anteriores', 'dados_novos'
        ]
    )
    writer.writeheader()
    for row in auditoria:
        writer.writerow(row)
    return output.getvalue()

# Para exportação PDF, utilize ReportLab (implementação pode ser feita sob demanda)
