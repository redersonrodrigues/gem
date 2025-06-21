"""
Relatório de escalas futuras (próximos 7, 15, 30 dias).
"""
from sqlalchemy.orm import Session
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from datetime import date, timedelta
import csv
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def consultar_escalas_futuras(session: Session, dias: int = 7):
    """
    Retorna todas as escalas de plantão e sobreaviso para os próximos N dias.
    """
    hoje = date.today()
    data_limite = hoje + timedelta(days=dias)
    plantoes = (
        session.query(EscalaPlantonista, Medico, Especializacao)
        .join(Medico, EscalaPlantonista.medico1_id == Medico.id)
        .join(Especializacao, Medico.especializacao_id == Especializacao.id)
        .filter(EscalaPlantonista.data >= hoje)
        .filter(EscalaPlantonista.data <= data_limite)
        .all()
    )
    sobreavisos = (
        session.query(EscalaSobreaviso, Medico, Especializacao)
        .join(Medico, EscalaSobreaviso.medico1_id == Medico.id)
        .join(Especializacao, EscalaSobreaviso.especializacao_id == Especializacao.id)
        .filter(EscalaSobreaviso.data_inicial >= hoje)
        .filter(EscalaSobreaviso.data_inicial <= data_limite)
        .all()
    )
    resultado = []
    for escala, medico, esp in plantoes:
        resultado.append({
            'tipo': 'plantao',
            'data': escala.data,
            'turno': escala.turno,
            'medico': medico.nome,
            'especializacao': esp.nome,
        })
    for escala, medico, esp in sobreavisos:
        resultado.append({
            'tipo': 'sobreaviso',
            'data_inicial': escala.data_inicial,
            'data_final': escala.data_final,
            'medico': medico.nome,
            'especializacao': esp.nome,
        })
    return resultado


def exportar_escalas_futuras_csv(dados):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Tipo', 'Data', 'Turno', 'Médico', 'Especialização', 'Data Final'])
    for item in dados:
        if item['tipo'] == 'plantao':
            writer.writerow([
                'Plantão', item['data'], item['turno'], item['medico'], item['especializacao'], ''
            ])
        else:
            writer.writerow([
                'Sobreaviso', item['data_inicial'], '', item['medico'], item['especializacao'], item['data_final']
            ])
    return output.getvalue()


def exportar_escalas_futuras_pdf(dados, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 40, "Relatório de Escalas Futuras")
    c.setFont("Helvetica", 10)
    y = height - 70
    headers = ['Tipo', 'Data', 'Turno', 'Médico', 'Especialização', 'Data Final']
    for i, h in enumerate(headers):
        c.drawString(30 + i*90, y, h)
    y -= 20
    for item in dados:
        if item['tipo'] == 'plantao':
            c.drawString(30, y, 'Plantão')
            c.drawString(120, y, str(item['data']))
            c.drawString(210, y, item['turno'])
            c.drawString(300, y, item['medico'])
            c.drawString(390, y, item['especializacao'])
            c.drawString(480, y, '')
        else:
            c.drawString(30, y, 'Sobreaviso')
            c.drawString(120, y, str(item['data_inicial']))
            c.drawString(210, y, '')
            c.drawString(300, y, item['medico'])
            c.drawString(390, y, item['especializacao'])
            c.drawString(480, y, str(item['data_final']))
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 70
    c.save()
    return filename
