"""
Tela de gestão de especializações - PyQt5
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QHBoxLayout, QLineEdit, QAbstractItemView, QHeaderView, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from app.components.ui_elements import PrimaryButton, SearchField, StyledTable
from app.components.icon_helper import get_icon
from app.components.notifier import Notifier
from app.utils.integrity_checker import IntegrityChecker
from app.utils.data_io import export_to_csv, import_from_csv, export_to_json, import_from_json
from app.components.ui_logger import log_action
from app.crud import get_especializacoes, create_especializacao, update_especializacao, delete_especializacao
from app.components.message_manager import MessageManager
import os

class EspecializacoesView(QWidget):
    def __init__(self, parent=None, integrity_checker: IntegrityChecker = None, perfil=None):
        super().__init__(parent)
        self.setObjectName("especializacoes_view")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(32, 32, 32, 32)
        self.layout.setSpacing(18)
        self.setLayout(self.layout)
        self.setStyleSheet('background-color: white;')
        self.integrity_checker = integrity_checker
        self.perfil = perfil
        self.init_ui()
        self.load_data()

    def init_ui(self):
        title = QLabel("Gestão de Especializações")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #1976d2; margin-bottom: 18px;")
        self.layout.addWidget(title)
        # Barra de busca
        search_layout = QHBoxLayout()
        class UpperSearchField(SearchField):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.textChanged.connect(self.to_upper_and_search)
            def to_upper_and_search(self, text):
                cursor_pos = self.cursorPosition()
                self.setText(text.upper())
                self.setCursorPosition(cursor_pos)
                if hasattr(self.parentWidget(), 'buscar_especializacao'):
                    self.parentWidget().buscar_especializacao()
        self.search_input = UpperSearchField("Buscar especialização...")
        search_btn = PrimaryButton("Buscar")
        search_btn.setIcon(get_icon("search"))
        search_btn.clicked.connect(self.buscar_especializacao)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        self.layout.addLayout(search_layout)
        # Tabela de especializações
        self.table = StyledTable(0, 2)
        self.table.setHorizontalHeaderLabels(["Nome", "Ação"])
        self.table.setStyleSheet('font-size: 15px; background: #fff;')
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        # Botões de ação centralizados
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        add_btn = PrimaryButton("Adicionar Especialização")
        add_btn.setIcon(get_icon("add"))
        add_btn.clicked.connect(self.adicionar_especializacao)
        btn_layout.addWidget(add_btn)
        export_csv_btn = PrimaryButton("Exportar CSV")
        export_csv_btn.setIcon(get_icon("download"))
        export_csv_btn.clicked.connect(self.exportar_csv)
        btn_layout.addWidget(export_csv_btn)
        import_csv_btn = PrimaryButton("Importar CSV")
        import_csv_btn.setIcon(get_icon("upload"))
        import_csv_btn.clicked.connect(self.importar_csv)
        btn_layout.addWidget(import_csv_btn)
        btn_layout.addStretch()
        self.layout.addLayout(btn_layout)
        self.table.cellClicked.connect(self.handle_table_action)

    def load_data(self):
        self.table.setRowCount(0)
        self._especializacoes = get_especializacoes()
        for esp in self._especializacoes:
            self.add_row(esp)

    def add_row(self, esp):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(esp.nome))
        # Coluna ação: editar e excluir
        pen_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'icons', 'solid', 'pen.svg'))
        trash_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'icons', 'solid', 'trash.svg'))
        edit_icon = QIcon(pen_path)
        del_icon = QIcon(trash_path)
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(6)
        btn_edit = QPushButton()
        btn_edit.setIcon(edit_icon)
        btn_edit.setToolTip('Editar')
        btn_edit.setFixedSize(28, 28)
        btn_edit.setStyleSheet('background-color: #FFD600; color: black; border-radius: 6px;')  # amarelo
        btn_edit.setIconSize(btn_edit.size() - QSize(8, 8))
        btn_edit.setStyleSheet('background-color: #FFD600; color: black; border-radius: 6px;')
        btn_edit.setProperty('class', 'edit-btn')
        btn_edit.setStyleSheet('background-color: #FFD600; color: black; border-radius: 6px;')
        btn_edit.clicked.connect(lambda _, e=esp: self.editar_especializacao(e))
        btn_del = QPushButton()
        btn_del.setIcon(del_icon)
        btn_del.setToolTip('Excluir')
        btn_del.setFixedSize(28, 28)
        btn_del.setIconSize(btn_del.size() - QSize(8, 8))
        btn_del.setStyleSheet('background-color: #d32f2f; color: white; border-radius: 6px;')  # vermelho
        btn_del.setProperty('class', 'del-btn')
        btn_del.clicked.connect(lambda _, e=esp: self.excluir_especializacao_dialog(e))
        action_layout.addWidget(btn_edit)
        action_layout.addWidget(btn_del)
        action_layout.addStretch()
        self.table.setCellWidget(row, 1, action_widget)

    def buscar_especializacao(self):
        termo = self.search_input.text().strip().upper()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                visivel = termo in item.text().upper()
                self.table.setRowHidden(row, not visivel)
        if not termo:
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)

    def adicionar_especializacao(self):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
        class UpperLineEdit(QLineEdit):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.textChanged.connect(self.to_upper)
            def to_upper(self, text):
                cursor_pos = self.cursorPosition()
                self.setText(text.upper())
                self.setCursorPosition(cursor_pos)
        class AddDialog(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle('Adicionar Especialização')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input = UpperLineEdit()
                self.input.setPlaceholderText('NOME DA ESPECIALIZAÇÃO')
                layout.addWidget(QLabel('Nome da especialização:'))
                layout.addWidget(self.input)
                btn_layout = QHBoxLayout()
                from app.components.ui_elements import PrimaryButton
                btn_ok = PrimaryButton('Confirmar')
                btn_cancel = PrimaryButton('Cancelar')
                btn_ok.setStyleSheet('background-color: #388e3c; color: white; font-weight: bold;')
                btn_cancel.setStyleSheet('background-color: #d32f2f; color: white; font-weight: bold;')
                btn_ok.clicked.connect(self.accept)
                btn_cancel.clicked.connect(self.reject)
                btn_layout.addWidget(btn_ok)
                btn_layout.addWidget(btn_cancel)
                layout.addLayout(btn_layout)
                self.setLayout(layout)
        dialog = AddDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.input.text().strip():
            nome = dialog.input.text().strip()
            user_id = getattr(self.parent(), 'usuario', None)
            if user_id and hasattr(user_id, 'id'):
                user_id = user_id.id
            elif hasattr(self, 'usuario') and hasattr(self.usuario, 'id'):
                user_id = self.usuario.id
            else:
                user_id = 1  # fallback para admin
            create_especializacao(nome, user_id)
            self.load_data()
            MessageManager.info(self, "Cadastro", "Especialização adicionada com sucesso.")

    def editar_especializacao(self, esp):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
        class UpperLineEdit(QLineEdit):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.textChanged.connect(self.to_upper)
            def to_upper(self, text):
                cursor_pos = self.cursorPosition()
                self.setText(text.upper())
                self.setCursorPosition(cursor_pos)
        class EditDialog(QDialog):
            def __init__(self, parent=None, nome_atual=""):
                super().__init__(parent)
                self.setWindowTitle('Editar Especialização')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input = UpperLineEdit()
                self.input.setText(nome_atual)
                layout.addWidget(QLabel('Novo nome:'))
                layout.addWidget(self.input)
                btn_layout = QHBoxLayout()
                from app.components.ui_elements import PrimaryButton
                btn_ok = PrimaryButton('Confirmar')
                btn_cancel = PrimaryButton('Cancelar')
                btn_ok.setStyleSheet('background-color: #388e3c; color: white; font-weight: bold;')
                btn_cancel.setStyleSheet('background-color: #d32f2f; color: white; font-weight: bold;')
                btn_ok.clicked.connect(self.accept)
                btn_cancel.clicked.connect(self.reject)
                btn_layout.addWidget(btn_ok)
                btn_layout.addWidget(btn_cancel)
                layout.addLayout(btn_layout)
                self.setLayout(layout)
        dialog = EditDialog(self, esp.nome)
        if dialog.exec_() == QDialog.Accepted and dialog.input.text().strip():
            nome = dialog.input.text().strip()
            user_id = getattr(self.parent(), 'usuario', None)
            if user_id and hasattr(user_id, 'id'):
                user_id = user_id.id
            elif hasattr(self, 'usuario') and hasattr(self.usuario, 'id'):
                user_id = self.usuario.id
            else:
                user_id = 1  # fallback para admin
            update_especializacao(esp.id, nome, user_id)
            self.load_data()
            MessageManager.info(self, "Edição", "Especialização editada com sucesso.")

    def excluir_especializacao_dialog(self, esp):
        # Diálogo customizado com botões estilizados
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
        class ConfirmDialog(QDialog):
            def __init__(self, parent=None, nome=""):
                super().__init__(parent)
                self.setWindowTitle('Confirmação')
                self.setModal(True)
                layout = QVBoxLayout()
                label = QLabel(f"Deseja excluir a especialização '{nome}'?")
                layout.addWidget(label)
                btn_layout = QHBoxLayout()
                btn_yes = QPushButton('Sim')
                btn_no = QPushButton('Não')
                btn_yes.setStyleSheet('background-color: #1976d2; color: white; font-weight: bold;')
                btn_no.setStyleSheet('background-color: #d32f2f; color: white; font-weight: bold;')
                btn_yes.clicked.connect(self.accept)
                btn_no.clicked.connect(self.reject)
                btn_layout.addWidget(btn_yes)
                btn_layout.addWidget(btn_no)
                layout.addLayout(btn_layout)
                self.setLayout(layout)
        dialog = ConfirmDialog(self, esp.nome)
        if dialog.exec_() == QDialog.Accepted:
            self.excluir_especializacao(esp.id)

    def excluir_especializacao(self, especializacao_id: int):
        if self.perfil != 'admin':
            MessageManager.warning(self, "Acesso negado", "Você não tem permissão para excluir especializações.")
            return
        if self.integrity_checker and not self.integrity_checker.can_delete_especializacao(especializacao_id):
            MessageManager.warning(self, "Exclusão não permitida", "Existem médicos vinculados a esta especialização.")
            return
        user_id = getattr(self.parent(), 'usuario', None)
        if user_id and hasattr(user_id, 'id'):
            user_id = user_id.id
        elif hasattr(self, 'usuario') and hasattr(self.usuario, 'id'):
            user_id = self.usuario.id
        else:
            user_id = 1  # fallback para admin
        delete_especializacao(especializacao_id, user_id)
        self.load_data()
        MessageManager.info(self, "Exclusão", "Especialização excluída com sucesso.")

    def handle_table_action(self, row, col):
        # Não faz nada, pois os botões já têm seus próprios slots
        pass

    def exportar_csv(self):
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            linha = [self.table.item(row, col).text() if self.table.item(row, col) else '' for col in range(self.table.columnCount())]
            data.append(linha)
        if export_to_csv(self, headers, data):
            MessageManager.info(self, "Exportação", "Especializações exportadas com sucesso.")
            log_action(self.perfil, 'export', 'especializacao', details='exportação em lote', result='sucesso')

    def importar_csv(self):
        rows = import_from_csv(self)
        if not rows:
            return
        import_ok = True
        for row in rows[1:]:
            if not all(row):
                MessageManager.warning(self, "Importação", f"Dados incompletos na linha: {row}")
                import_ok = False
                continue
            # Integridade: checar duplicidade
            for i in range(self.table.rowCount()):
                if self.table.item(i, 0) and self.table.item(i, 0).text() == row[0]:
                    MessageManager.warning(self, "Importação", f"Especialização já existe: {row[0]}")
                    import_ok = False
                    break
            else:
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                for col, value in enumerate(row):
                    self.table.setItem(row_idx, col, QTableWidgetItem(value))
        if import_ok:
            MessageManager.info(self, "Importação", "Especializações importadas com sucesso.")
            log_action(self.perfil, 'import', 'especializacao', details='importação em lote', result='sucesso')
        else:
            log_action(self.perfil, 'import', 'especializacao', details='importação com erros', result='erro')
