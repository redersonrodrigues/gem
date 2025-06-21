"""
Relatório de carga horária por médico: total de plantões, horas e turnos.
"""
from sqlalchemy.orm import Session
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico
from sqlalchemy import func
import csv
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime


def consulta_carga_horaria_por_medico(db: Session, mes: int, ano: int):
    """
    Retorna lista de médicos com total de plantões, horas e turnos no mês/ano informado.
    """
    # Plantões
    plantao_query = (
        db.query(
            Medico.id.label('medico_id'),
            Medico.nome.label('nome'),
            func.count(EscalaPlantonista.id).label('total_plantoes'),
            (func.count(EscalaPlantonista.id) * 12).label('total_horas'),
            func.count(func.distinct(EscalaPlantonista.turno)).label('total_turnos'),
        )
        .join(EscalaPlantonista, EscalaPlantonista.medico1_id == Medico.id)
        .filter(func.extract('month', EscalaPlantonista.data) == mes)
        .filter(func.extract('year', EscalaPlantonista.data) == ano)
        .group_by(Medico.id)
    )
    # Sobreavisos (opcional: pode ser somado ao total)
    sobreaviso_query = (
        db.query(
            Medico.id.label('medico_id'),
            func.count(EscalaSobreaviso.id).label('total_sobreavisos'),
            (func.count(EscalaSobreaviso.id) * 12).label('total_horas_sobreaviso'),
        )
        .join(EscalaSobreaviso, EscalaSobreaviso.medico1_id == Medico.id)
        .filter(func.extract('month', EscalaSobreaviso.data_inicial) == mes)
        .filter(func.extract('year', EscalaSobreaviso.data_inicial) == ano)
        .group_by(Medico.id)
    )
    # Monta dicionário por médico
    resultado = {}
    for row in plantao_query:
        resultado[row.medico_id] = {
            'nome': row.nome,
            'total_plantoes': row.total_plantoes or 0,
            'total_horas': float(row.total_horas or 0),
            'total_turnos': row.total_turnos or 0,
            'total_sobreavisos': 0,
            'total_horas_sobreaviso': 0.0,
        }
    for row in sobreaviso_query:
        if row.medico_id in resultado:
            resultado[row.medico_id]['total_sobreavisos'] = row.total_sobreavisos or 0
            resultado[row.medico_id]['total_horas_sobreaviso'] = float(row.total_horas_sobreaviso or 0)
        else:
            medico = db.query(Medico).filter_by(id=row.medico_id).first()
            resultado[row.medico_id] = {
                'nome': medico.nome if medico else '',
                'total_plantoes': 0,
                'total_horas': 0.0,
                'total_turnos': 0,
                'total_sobreavisos': row.total_sobreavisos or 0,
                'total_horas_sobreaviso': float(row.total_horas_sobreaviso or 0),
            }
    return list(resultado.values())


def exportar_carga_horaria_csv(dados, mes, ano):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Nome do Médico', 'Total Plantões', 'Total Horas Plantão', 'Total Turnos',
        'Total Sobreavisos', 'Total Horas Sobreaviso',
    ])
    for item in dados:
        writer.writerow([
            item['nome'],
            item['total_plantoes'],
            f"{item['total_horas']:.2f}",
            item['total_turnos'],
            item['total_sobreavisos'],
            f"{item['total_horas_sobreaviso']:.2f}",
        ])
    return output.getvalue()


def exportar_carga_horaria_pdf(dados, mes, ano, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 40, f"Relatório de Carga Horária por Médico - {mes:02d}/{ano}")
    c.setFont("Helvetica", 10)
    y = height - 70
    headers = [
        'Nome do Médico', 'Total Plantões', 'Total Horas Plantão', 'Total Turnos',
        'Total Sobreavisos', 'Total Horas Sobreaviso',
    ]
    for i, h in enumerate(headers):
        c.drawString(30 + i*100, y, h)
    y -= 20
    for item in dados:
        c.drawString(30, y, str(item['nome']))
        c.drawString(130, y, str(item['total_plantoes']))
        c.drawString(230, y, f"{item['total_horas']:.2f}")
        c.drawString(330, y, str(item['total_turnos']))
        c.drawString(430, y, str(item['total_sobreavisos']))
        c.drawString(530, y, f"{item['total_horas_sobreaviso']:.2f}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 70
    c.save()
    return filename
