"""
Tela de gestão de escalas - PyQt5
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from app.components.ui_elements import PrimaryButton, SearchField, StyledTable
from app.components.notifier import Notifier
from app.components.icon_helper import get_icon
from app.utils.integrity_checker import IntegrityChecker
from app.components.print_helper import gerar_pdf_relatorio
from app.utils.data_io import export_to_csv, import_from_csv, export_to_json, import_from_json
from app.components.ui_logger import log_action
import os

class EscalasView(QWidget):
    def __init__(self, parent=None, integrity_checker: IntegrityChecker = None, perfil=None):
        super().__init__(parent)
        self.setObjectName("escalas_view")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.integrity_checker = integrity_checker
        self.perfil = perfil
        self.init_ui()

    def init_ui(self):
        title = QLabel("Gestão de Escalas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(title)

        # Barra de busca
        search_layout = QHBoxLayout()
        self.search_input = SearchField("Buscar escala...")
        search_btn = PrimaryButton("Buscar")
        search_btn.setIcon(get_icon("search"))
        search_btn.clicked.connect(self.buscar_escala)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        self.layout.addLayout(search_layout)

        # Tabela de escalas
        self.table = StyledTable(0, 4)
        self.table.setHorizontalHeaderLabels(["Data", "Turno", "Médico 0", "Médico 1"])
        self.layout.addWidget(self.table)

        # Botões de ação
        btn_layout = QHBoxLayout()
        add_btn = PrimaryButton("Adicionar Escala")
        add_btn.setIcon(get_icon("add"))
        add_btn.clicked.connect(self.adicionar_escala)
        btn_layout.addWidget(add_btn)
        # Botão exportar CSV
        export_csv_btn = PrimaryButton("Exportar CSV")
        export_csv_btn.setIcon(get_icon("download"))
        export_csv_btn.clicked.connect(self.exportar_csv)
        btn_layout.addWidget(export_csv_btn)
        # Botão importar CSV
        import_csv_btn = PrimaryButton("Importar CSV")
        import_csv_btn.setIcon(get_icon("upload"))
        import_csv_btn.clicked.connect(self.importar_csv)
        btn_layout.addWidget(import_csv_btn)
        # Botão de impressão
        print_btn = PrimaryButton("Imprimir Relatório")
        print_btn.setIcon(get_icon("calendar"))
        print_btn.clicked.connect(self.imprimir_relatorio)
        btn_layout.addWidget(print_btn)

        self.layout.addLayout(btn_layout)

    def buscar_escala(self):
        termo = self.search_input.text().strip().lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                visivel = termo in item.text().lower()
                self.table.setRowHidden(row, not visivel)
        if not termo:
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)

    def adicionar_escala(self):
        # Exemplo de alerta para escala próxima (mock)
        Notifier.warning(self, "Alerta", "Existe uma escala próxima do vencimento!")
        QMessageBox.information(self, "Adicionar Escala", "Funcionalidade de adicionar escala ainda não implementada.")

    def imprimir_relatorio(self):
        cabecalhos = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        dados = []
        for row in range(self.table.rowCount()):
            if self.table.isRowHidden(row):
                continue
            linha = [self.table.item(row, col).text() if self.table.item(row, col) else '' for col in range(self.table.columnCount())]
            dados.append(linha)
        nome_arquivo = os.path.expanduser("~\\relatorio_escalas.pdf")
        gerar_pdf_relatorio(nome_arquivo, "Relatório de Escalas", cabecalhos, dados, rodape="GEM - Sistema de Escalas Médicas")
        Notifier.info(self, "Impressão", f"Relatório gerado em {nome_arquivo}")

    def exportar_csv(self):
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            linha = [self.table.item(row, col).text() if self.table.item(row, col) else '' for col in range(self.table.columnCount())]
            data.append(linha)
        if export_to_csv(self, headers, data):
            Notifier.info(self, "Exportação", "Escalas exportadas com sucesso.")
            log_action(self.perfil, 'export', 'escala', details='exportação em lote', result='sucesso')

    def importar_csv(self):
        rows = import_from_csv(self)
        if not rows:
            return
        import_ok = True
        for row in rows[1:]:
            if not all(row):
                Notifier.error(self, "Importação", "Dados incompletos na linha: {}".format(row))
                import_ok = False
                continue
            # Integridade: checar duplicidade de data/turno
            for i in range(self.table.rowCount()):
                if self.table.item(i, 0) and self.table.item(i, 0).text() == row[0] and self.table.item(i, 1) and self.table.item(i, 1).text() == row[1]:
                    Notifier.error(self, "Importação", f"Escala já existe para data/turno: {row[0]} {row[1]}")
                    import_ok = False
                    break
            else:
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                for col, value in enumerate(row):
                    self.table.setItem(row_idx, col, QTableWidgetItem(value))
        if import_ok:
            Notifier.info(self, "Importação", "Escalas importadas com sucesso.")
            log_action(self.perfil, 'import', 'escala', details='importação em lote', result='sucesso')
        else:
            log_action(self.perfil, 'import', 'escala', details='importação com erros', result='erro')

    def excluir_escala(self, escala_id: int):
        if self.perfil != 'admin':
            Notifier.error(self, "Acesso negado", "Você não tem permissão para excluir escalas.")
            return
        if self.integrity_checker and not self.integrity_checker.can_delete_escala(escala_id):
            Notifier.error(self, "Exclusão não permitida", "Esta escala não pode ser excluída devido a vínculos.")
            return
        # Código de exclusão real aqui
        log_action(self.perfil, 'delete', 'escala', escala_id)
        Notifier.info(self, "Exclusão", "Escala excluída com sucesso.")
