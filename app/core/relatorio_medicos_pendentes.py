"""
Relatório: Listagem de médicos com pendências de documentação ou cadastro.
Pendências: nome vazio/nulo, especialização não definida, status nulo/vazio.
"""
from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.models.especializacao import Especializacao
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def consultar_medicos_pendentes(session: Session):
    query = (
        session.query(Medico, Especializacao)
        .join(Especializacao, Medico.especializacao_id == Especializacao.id)
        .filter(
            (Medico.nome == None) | (Medico.nome == "") |
            (Medico.especializacao_id == None) |
            (Medico.status == None) | (Medico.status == "")
        )
    )
    resultado = []
    for medico, esp in query.all():
        resultado.append({
            'nome': medico.nome,
            'nome_pj': medico.nome_pj,
            'especializacao': esp.nome if esp else None,
            'status': medico.status.value if hasattr(medico.status, 'value') else str(medico.status),
        })
    return resultado

def exportar_medicos_pendentes_csv(dados, caminho):
    if not dados:
        return
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)

def exportar_medicos_pendentes_pdf(dados, caminho):
    c = canvas.Canvas(caminho, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, "Médicos com Pendências de Cadastro/Documentação")
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
