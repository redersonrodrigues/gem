"""
Helper para geração e impressão de relatórios em PDF usando ReportLab
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def gerar_pdf_relatorio(nome_arquivo, titulo, cabecalhos, dados, rodape=None, logotipo=None):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    width, height = A4
    y = height - 50
    if logotipo and os.path.exists(logotipo):
        c.drawImage(logotipo, 40, y - 40, width=80, height=40)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(140, y, titulo)
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    for i, cab in enumerate(cabecalhos):
        c.drawString(40 + i*120, y, cab)
    y -= 20
    c.setFont("Helvetica", 11)
    for linha in dados:
        for i, valor in enumerate(linha):
            c.drawString(40 + i*120, y, str(valor))
        y -= 18
        if y < 80:
            c.showPage()
            y = height - 50
    if rodape:
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(40, 40, rodape)
    c.save()
    return nome_arquivo
