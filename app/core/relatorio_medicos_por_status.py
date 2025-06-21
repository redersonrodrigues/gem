"""
Relatório de médicos por status (ativos, inativos, afastados).
"""
from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.models.especializacao import Especializacao
import csv
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def consultar_medicos_por_status(session: Session, status: str = None):
    """
    Retorna todos os médicos filtrando por status (ativo, inativo, afastado) se informado.
    """
    query = session.query(Medico, Especializacao).join(Especializacao, Medico.especializacao_id == Especializacao.id)
    if status:
        query = query.filter(Medico.status == status)
    resultado = []
    for medico, esp in query.all():
        resultado.append({
            'nome': medico.nome,
            'nome_pj': medico.nome_pj,
            'especializacao': esp.nome,
            'status': medico.status.value if hasattr(medico.status, 'value') else str(medico.status),
        })
    return resultado


def exportar_medicos_por_status_csv(dados):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Nome', 'Nome PJ', 'Especialização', 'Status'])
    for item in dados:
        writer.writerow([
            item['nome'],
            item['nome_pj'] or '',
            item['especializacao'],
            item['status'],
        ])
    return output.getvalue()


def exportar_medicos_por_status_pdf(dados, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 40, "Relatório de Médicos por Status")
    c.setFont("Helvetica", 10)
    y = height - 70
    headers = ['Nome', 'Nome PJ', 'Especialização', 'Status']
    for i, h in enumerate(headers):
        c.drawString(30 + i*120, y, h)
    y -= 20
    for item in dados:
        c.drawString(30, y, item['nome'])
        c.drawString(150, y, item['nome_pj'] or '')
        c.drawString(270, y, item['especializacao'])
        c.drawString(390, y, item['status'])
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 70
    c.save()
    return filename
