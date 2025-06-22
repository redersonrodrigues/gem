"""
Tela de gestão de especializações - PyQt5
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from app.components.ui_elements import PrimaryButton, SearchField, StyledTable
from app.components.icon_helper import get_icon
from app.components.notifier import Notifier
from app.utils.integrity_checker import IntegrityChecker
from app.utils.data_io import export_to_csv, import_from_csv, export_to_json, import_from_json
from app.components.ui_logger import log_action

class EspecializacoesView(QWidget):
    def __init__(self, parent=None, integrity_checker: IntegrityChecker = None, perfil=None):
        super().__init__(parent)
        self.setObjectName("especializacoes_view")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.integrity_checker = integrity_checker
        self.perfil = perfil
        self.init_ui()

    def init_ui(self):
        title = QLabel("Gestão de Especializações")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(title)

        # Barra de busca
        search_layout = QHBoxLayout()
        self.search_input = SearchField("Buscar especialização...")
        search_btn = PrimaryButton("Buscar")
        search_btn.setIcon(get_icon("search"))
        search_btn.clicked.connect(self.buscar_especializacao)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        self.layout.addLayout(search_layout)

        # Tabela de especializações
        self.table = StyledTable(0, 1)
        self.table.setHorizontalHeaderLabels(["Nome"])
        self.layout.addWidget(self.table)

        # Botões de ação
        btn_layout = QHBoxLayout()
        add_btn = PrimaryButton("Adicionar Especialização")
        add_btn.setIcon(get_icon("add"))
        add_btn.clicked.connect(self.adicionar_especializacao)
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
        self.layout.addLayout(btn_layout)

    def buscar_especializacao(self):
        termo = self.search_input.text().strip().lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                visivel = termo in item.text().lower()
                self.table.setRowHidden(row, not visivel)
        if not termo:
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)

    def adicionar_especializacao(self):
        QMessageBox.information(self, "Adicionar Especialização", "Funcionalidade de adicionar especialização ainda não implementada.")

    def excluir_especializacao(self, especializacao_id: int):
        if self.perfil != 'admin':
            Notifier.error(self, "Acesso negado", "Você não tem permissão para excluir especializações.")
            return
        if self.integrity_checker and not self.integrity_checker.can_delete_especializacao(especializacao_id):
            Notifier.error(self, "Exclusão não permitida", "Existem médicos vinculados a esta especialização.")
            return
        # Código de exclusão real aqui
        log_action(self.perfil, 'delete', 'especializacao', especializacao_id)
        Notifier.info(self, "Exclusão", "Especialização excluída com sucesso.")

    def exportar_csv(self):
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            linha = [self.table.item(row, col).text() if self.table.item(row, col) else '' for col in range(self.table.columnCount())]
            data.append(linha)
        if export_to_csv(self, headers, data):
            Notifier.info(self, "Exportação", "Especializações exportadas com sucesso.")
            log_action(self.perfil, 'export', 'especializacao', details='exportação em lote', result='sucesso')

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
            # Integridade: checar duplicidade
            for i in range(self.table.rowCount()):
                if self.table.item(i, 0) and self.table.item(i, 0).text() == row[0]:
                    Notifier.error(self, "Importação", f"Especialização já existe: {row[0]}")
                    import_ok = False
                    break
            else:
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                for col, value in enumerate(row):
                    self.table.setItem(row_idx, col, QTableWidgetItem(value))
        if import_ok:
            Notifier.info(self, "Importação", "Especializações importadas com sucesso.")
            log_action(self.perfil, 'import', 'especializacao', details='importação em lote', result='sucesso')
        else:
            log_action(self.perfil, 'import', 'especializacao', details='importação com erros', result='erro')
