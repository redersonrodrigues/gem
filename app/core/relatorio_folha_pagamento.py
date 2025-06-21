"""
Relatório: Escalas exportável para folha de pagamento
Gera relatório de escalas (plantonistas e sobreaviso) com campos para folha de pagamento, exportável em CSV/PDF.
"""
from datetime import date
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico
from app.models.especializacao import Especializacao
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def consultar_escalas_folha_pagamento(session: Session, data_inicio: date, data_fim: date) -> List[Dict]:
    """Consulta todas as escalas do período, formatando para folha de pagamento."""
    plantoes = (
        session.query(
            EscalaPlantonista.data,
            EscalaPlantonista.turno,
            Medico.nome.label("medico"),
            Medico.nome_pj.label("nome_pj"),
            Especializacao.nome.label("especializacao"),
        )
        .join(Medico, EscalaPlantonista.medico1_id == Medico.id)
        .join(Especializacao, Medico.especializacao_id == Especializacao.id)
        .filter(EscalaPlantonista.data >= data_inicio)
        .filter(EscalaPlantonista.data <= data_fim)
    )
    sobreavisos = (
        session.query(
            EscalaSobreaviso.data_inicial.label("data"),
            None,  # turno não se aplica
            Medico.nome.label("medico"),
            Medico.nome_pj.label("nome_pj"),
            Especializacao.nome.label("especializacao"),
        )
        .join(Medico, EscalaSobreaviso.medico1_id == Medico.id)
        .join(Especializacao, EscalaSobreaviso.especializacao_id == Especializacao.id)
        .filter(EscalaSobreaviso.data_inicial >= data_inicio)
        .filter(EscalaSobreaviso.data_inicial <= data_fim)
    )
    dados = []
    for row in plantoes:
        d = dict(row._mapping)
        d["tipo"] = "Plantão"
        dados.append(d)
    for row in sobreavisos:
        d = dict(row._mapping)
        d["turno"] = None
        d["tipo"] = "Sobreaviso"
        dados.append(d)
    dados.sort(key=lambda x: x["data"])
    return dados

def exportar_folha_pagamento_csv(dados: List[Dict], caminho: str):
    if not dados:
        return
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["data", "turno", "medico", "nome_pj", "especializacao", "tipo"])
        writer.writeheader()
        for row in dados:
            writer.writerow(row)

def exportar_folha_pagamento_pdf(dados: List[Dict], caminho: str):
    c = canvas.Canvas(caminho, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, "Escalas para Folha de Pagamento")
    c.setFont("Helvetica", 10)
    y = height - 70
    if not dados:
        c.drawString(40, y, "Nenhum registro encontrado.")
    else:
        headers = ["data", "turno", "medico", "nome_pj", "especializacao", "tipo"]
        for i, h in enumerate(headers):
            c.drawString(40 + i * 90, y, h)
        y -= 20
        for row in dados:
            for i, h in enumerate(headers):
                valor = row[h] if row[h] is not None else ""
                c.drawString(40 + i * 90, y, str(valor))
            y -= 18
            if y < 50:
                c.showPage()
                y = height - 70
    c.save()
