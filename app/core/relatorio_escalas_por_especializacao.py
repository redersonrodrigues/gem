"""
Relatório: Relatório mensal de escalas por especialização
Retorna a quantidade de plantões e sobreavisos por especialização em um mês.
"""
from datetime import date
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from sqlalchemy import func
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def relatorio_escalas_por_especializacao(session: Session, ano: int, mes: int) -> List[Dict]:
    """
    Retorna lista de dicionários com especialização, quantidade de plantões e sobreavisos no mês.
    """
    data_inicio = date(ano, mes, 1)
    if mes == 12:
        data_fim = date(ano + 1, 1, 1)
    else:
        data_fim = date(ano, mes + 1, 1)

    # Plantões agrupados por especialização
    plantao = (
        session.query(
            Especializacao.nome.label('especializacao'),
            func.count(EscalaPlantonista.id).label('qtd_plantao')
        )
        .join(Medico, Medico.especializacao_id == Especializacao.id)
        .join(EscalaPlantonista, EscalaPlantonista.medico1_id == Medico.id)
        .filter(EscalaPlantonista.data >= data_inicio, EscalaPlantonista.data < data_fim)
        .group_by(Especializacao.nome)
        .all()
    )

    # Sobreavisos agrupados por especialização
    sobreaviso = (
        session.query(
            Especializacao.nome.label('especializacao'),
            func.count(EscalaSobreaviso.id).label('qtd_sobreaviso')
        )
        .join(EscalaSobreaviso, EscalaSobreaviso.especializacao_id == Especializacao.id)
        .filter(EscalaSobreaviso.data_inicial < data_fim, EscalaSobreaviso.data_final >= data_inicio)
        .group_by(Especializacao.nome)
        .all()
    )

    # Unir resultados
    resultado = {}
    for row in plantao:
        resultado[row.especializacao] = {'especializacao': row.especializacao, 'qtd_plantao': row.qtd_plantao, 'qtd_sobreaviso': 0}
    for row in sobreaviso:
        if row.especializacao in resultado:
            resultado[row.especializacao]['qtd_sobreaviso'] = row.qtd_sobreaviso
        else:
            resultado[row.especializacao] = {'especializacao': row.especializacao, 'qtd_plantao': 0, 'qtd_sobreaviso': row.qtd_sobreaviso}
    return list(resultado.values())

def exportar_csv(dados, caminho):
    if not dados:
        return
    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['especializacao', 'qtd_plantao', 'qtd_sobreaviso'])
        writer.writeheader()
        for row in dados:
            writer.writerow(row)

def exportar_pdf(dados, caminho):
    c = canvas.Canvas(caminho, pagesize=A4)
    c.setFont('Helvetica', 12)
    c.drawString(50, 800, 'Relatório Mensal de Escalas por Especialização')
    y = 770
    c.drawString(50, y, 'Especialização')
    c.drawString(250, y, 'Qtd Plantão')
    c.drawString(350, y, 'Qtd Sobreaviso')
    y -= 20
    for row in dados:
        c.drawString(50, y, str(row['especializacao']))
        c.drawString(250, y, str(row['qtd_plantao']))
        c.drawString(350, y, str(row['qtd_sobreaviso']))
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()
