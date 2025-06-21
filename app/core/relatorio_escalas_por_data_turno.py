"""
Relatório: Listagem de escalas por data e turno
Lista todas as escalas de plantonistas agrupadas por data e turno, mostrando os médicos escalados em cada turno. Exportável em CSV/PDF.
"""
from sqlalchemy.orm import Session, aliased
from app.models.escala_plantonista import EscalaPlantonista
from app.models.medico import Medico
from datetime import date
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from typing import List, Dict

def listar_escalas_por_data_turno(session: Session, data_inicio: date = None, data_fim: date = None) -> List[Dict]:
    """Retorna lista de escalas agrupadas por data e turno."""
    Medico2 = aliased(Medico)
    query = session.query(
        EscalaPlantonista.data,
        EscalaPlantonista.turno,
        Medico.nome.label("medico1"),
        Medico2.nome.label("medico2")
    ).join(Medico, EscalaPlantonista.medico1_id == Medico.id)
    query = query.outerjoin(Medico2, EscalaPlantonista.medico2_id == Medico2.id)
    if data_inicio:
        query = query.filter(EscalaPlantonista.data >= data_inicio)
    if data_fim:
        query = query.filter(EscalaPlantonista.data <= data_fim)
    query = query.order_by(EscalaPlantonista.data, EscalaPlantonista.turno)
    resultado = []
    for row in query.all():
        d = dict(row._mapping)
        resultado.append(d)
    return resultado

def exportar_escalas_por_data_turno_csv(dados: List[Dict], caminho: str):
    if not dados:
        return
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["data", "turno", "medico1", "medico2"])
        writer.writeheader()
        writer.writerows(dados)

def exportar_escalas_por_data_turno_pdf(dados: List[Dict], caminho: str):
    c = canvas.Canvas(caminho, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, "Escalas por Data e Turno")
    c.setFont("Helvetica", 10)
    y = height - 70
    if not dados:
        c.drawString(40, y, "Nenhum registro encontrado.")
    else:
        headers = ["data", "turno", "medico1", "medico2"]
        for i, h in enumerate(headers):
            c.drawString(40 + i * 120, y, h)
        y -= 20
        for row in dados:
            for i, h in enumerate(headers):
                valor = row[h] if row[h] is not None else ""
                c.drawString(40 + i * 120, y, str(valor))
            y -= 18
            if y < 50:
                c.showPage()
                y = height - 70
    c.save()
