"""
Geração de relatório mensal de escala de plantonistas (PDF/CSV).
"""
from datetime import date
from sqlalchemy.orm import Session
from app.models.escala_plantonista import EscalaPlantonista
from app.models.medico import Medico
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def dados_escala_plantonistas(session: Session, ano: int, mes: int):
    """
    Retorna lista de plantões do mês, com médico, data e turno.
    """
    plantao = session.query(EscalaPlantonista).filter(
        EscalaPlantonista.data >= date(ano, mes, 1),
        EscalaPlantonista.data < date(ano + (mes // 12), (mes % 12) + 1, 1)
    ).all()
    dados = []
    for p in plantao:
        medico = session.query(Medico).get(p.medico1_id)
        dados.append({
            'data': p.data,
            'turno': p.turno,
            'medico': medico.nome if medico else 'N/A'
        })
    return dados

def exportar_csv(dados, caminho):
    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['data', 'turno', 'medico'])
        writer.writeheader()
        for row in dados:
            writer.writerow(row)

def exportar_pdf(dados, caminho):
    c = canvas.Canvas(caminho, pagesize=A4)
    c.setFont('Helvetica', 12)
    c.drawString(50, 800, 'Relatório Mensal de Escala de Plantonistas')
    y = 770
    c.drawString(50, y, 'Data')
    c.drawString(150, y, 'Turno')
    c.drawString(250, y, 'Médico')
    y -= 20
    for row in dados:
        c.drawString(50, y, str(row['data']))
        c.drawString(150, y, row['turno'])
        c.drawString(250, y, row['medico'])
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()
