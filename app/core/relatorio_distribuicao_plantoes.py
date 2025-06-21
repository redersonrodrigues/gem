"""
Relatório de Distribuição de Plantões (Equidade entre Médicos)
"""
from sqlalchemy.orm import Session
from app.models.escala_plantonista import EscalaPlantonista
from app.models.medico import Medico
from collections import defaultdict
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

class RelatorioDistribuicaoPlantoes:
    def __init__(self, db_session: Session):
        self.db = db_session

    def gerar_relatorio(self, data_inicio, data_fim):
        """
        Retorna um dicionário com a quantidade de plantões por médico no período,
        permitindo avaliar a equidade da distribuição.
        """
        plantoes = (
            self.db.query(EscalaPlantonista)
            .filter(EscalaPlantonista.data >= data_inicio)
            .filter(EscalaPlantonista.data <= data_fim)
            .all()
        )
        distribuicao = defaultdict(int)
        for escala in plantoes:
            if escala.medico1_id:
                distribuicao[escala.medico1_id] += 1
            if escala.medico2_id:
                distribuicao[escala.medico2_id] += 1
        # Buscar nomes dos médicos
        medicos = {m.id: m.nome for m in self.db.query(Medico).all()}
        resultado = []
        for medico_id, qtd in distribuicao.items():
            resultado.append({
                'medico_id': medico_id,
                'nome': medicos.get(medico_id, 'Desconhecido'),
                'quantidade_plantoes': qtd
            })
        # Ordena por quantidade de plantões (ascendente)
        resultado.sort(key=lambda x: x['quantidade_plantoes'])
        return resultado

    def exportar_csv(self, data_inicio, data_fim, file_path):
        dados = self.gerar_relatorio(data_inicio, data_fim)
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['medico_id', 'nome', 'quantidade_plantoes'])
            writer.writeheader()
            for row in dados:
                writer.writerow(row)

    def exportar_pdf(self, data_inicio, data_fim, file_path):
        dados = self.gerar_relatorio(data_inicio, data_fim)
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        c.setFont('Helvetica-Bold', 14)
        c.drawString(50, height - 50, 'Relatório de Distribuição de Plantões')
        c.setFont('Helvetica', 10)
        y = height - 80
        c.drawString(50, y, f'Período: {data_inicio} a {data_fim}')
        y -= 30
        c.setFont('Helvetica-Bold', 10)
        c.drawString(50, y, 'Médico')
        c.drawString(250, y, 'Qtd. Plantões')
        c.setFont('Helvetica', 10)
        y -= 20
        for row in dados:
            c.drawString(50, y, row['nome'])
            c.drawString(250, y, str(row['quantidade_plantoes']))
            y -= 18
            if y < 50:
                c.showPage()
                y = height - 50
        c.save()
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())
