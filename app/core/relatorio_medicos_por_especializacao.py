"""
Relatório: Listagem de médicos por especialização
Gera relatório de todos os médicos agrupados por especialização, exportável em CSV/PDF.
"""
from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.models.especializacao import Especializacao
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from typing import List, Dict

def listar_medicos_por_especializacao(session: Session) -> List[Dict]:
    """Retorna lista de médicos agrupados por especialização."""
    query = (
        session.query(
            Especializacao.nome.label("especializacao"),
            Medico.nome.label("medico"),
            Medico.nome_pj.label("nome_pj"),
            Medico.status.label("status")
        )
        .join(Medico, Medico.especializacao_id == Especializacao.id)
        .order_by(Especializacao.nome, Medico.nome)
    )
    resultado = []
    for row in query.all():
        d = dict(row._mapping)
        # Garante que status seja sempre string (valor do Enum)
        d["status"] = str(d["status"]) if d["status"] is not None else None
        resultado.append(d)
    return resultado

def exportar_medicos_por_especializacao_csv(dados: List[Dict], caminho: str):
    if not dados:
        return
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["especializacao", "medico", "nome_pj", "status"])
        writer.writeheader()
        writer.writerows(dados)

def exportar_medicos_por_especializacao_pdf(dados: List[Dict], caminho: str):
    c = canvas.Canvas(caminho, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, "Médicos por Especialização")
    c.setFont("Helvetica", 10)
    y = height - 70
    if not dados:
        c.drawString(40, y, "Nenhum registro encontrado.")
    else:
        headers = ["especializacao", "medico", "nome_pj", "status"]
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
