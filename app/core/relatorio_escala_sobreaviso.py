"""
Relatório: Escala mensal de sobreaviso
Gera relatório mensal de sobreaviso por especialização e médico, exportável em PDF/CSV.
"""
from datetime import date
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico
from app.models.especializacao import Especializacao
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def consultar_sobreaviso_mes(session: Session, ano: int, mes: int) -> List[Dict]:
    """Consulta escalas de sobreaviso do mês, agrupando por especialização e médico."""
    query = (
        session.query(
            EscalaSobreaviso.data_inicial,
            EscalaSobreaviso.data_final,
            Medico.nome.label("medico"),
            Especializacao.nome.label("especializacao")
        )
        .join(Medico, EscalaSobreaviso.medico1_id == Medico.id)
        .join(Especializacao, EscalaSobreaviso.especializacao_id == Especializacao.id)
        .filter(EscalaSobreaviso.data_inicial >= date(ano, mes, 1))
        .filter(EscalaSobreaviso.data_inicial < date(ano + (mes // 12), (mes % 12) + 1, 1))
        .order_by(EscalaSobreaviso.data_inicial)
    )
    return [dict(row._mapping) for row in query.all()]


def consultar_sobreaviso_periodo(session: Session, data_inicio: date, data_fim: date) -> List[Dict]:
    """Consulta escalas de sobreaviso entre data_inicio e data_fim, agrupando por especialização e médico."""
    query = (
        session.query(
            EscalaSobreaviso.data_inicial,
            EscalaSobreaviso.data_final,
            Medico.nome.label("medico"),
            Especializacao.nome.label("especializacao")
        )
        .join(Medico, EscalaSobreaviso.medico1_id == Medico.id)
        .join(Especializacao, EscalaSobreaviso.especializacao_id == Especializacao.id)
        .filter(EscalaSobreaviso.data_inicial >= data_inicio)
        .filter(EscalaSobreaviso.data_final <= data_fim)
        .order_by(EscalaSobreaviso.data_inicial)
    )
    return [dict(row._mapping) for row in query.all()]


def exportar_csv(dados: List[Dict], caminho: str):
    """Exporta o relatório em CSV."""
    if not dados:
        return
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)


def exportar_pdf(dados: List[Dict], caminho: str):
    """Exporta o relatório em PDF."""
    c = canvas.Canvas(caminho, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, "Relatório Mensal de Sobreaviso")
    c.setFont("Helvetica", 10)
    y = height - 70
    if not dados:
        c.drawString(40, y, "Nenhum registro encontrado.")
    else:
        headers = list(dados[0].keys())
        for i, h in enumerate(headers):
            c.drawString(40 + i * 120, y, h)
        y -= 20
        for row in dados:
            for i, h in enumerate(headers):
                c.drawString(40 + i * 120, y, str(row[h]))
            y -= 18
            if y < 60:
                c.showPage()
                y = height - 40
    c.save()
