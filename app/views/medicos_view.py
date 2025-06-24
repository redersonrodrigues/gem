"""
Tela de gestão de médicos - PyQt5
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from app.components.ui_elements import PrimaryButton, SearchField, StyledTable
from app.components.validators import FormValidator
from app.components.icon_helper import get_icon
from app.components.notifier import Notifier
from app.utils.integrity_checker import IntegrityChecker
from app.components.ui_logger import log_action
from app.utils.data_io import export_to_csv, import_from_csv, export_to_json, import_from_json
from app.components.message_manager import MessageManager
from app.crud import get_medicos, get_especializacoes, create_medico, update_medico, delete_medico
import os

class MedicosView(QWidget):
    def __init__(self, parent=None, integrity_checker: IntegrityChecker = None, perfil=None):
        super().__init__(parent)
        self.setObjectName("medicos_view")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.integrity_checker = integrity_checker
        self.perfil = perfil
        self.init_ui()

    def init_ui(self):
        title = QLabel("Gestão de Médicos")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
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
                if hasattr(self.parentWidget(), 'buscar_medico'):
                    self.parentWidget().buscar_medico()
        self.search_input = UpperSearchField("Buscar médico pelo nome...")
        search_btn = PrimaryButton("Buscar")
        search_btn.setIcon(get_icon("search"))
        search_btn.clicked.connect(self.buscar_medico)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        self.layout.addLayout(search_layout)
        # Tabela de médicos
        self.table = StyledTable(0, 5)
        self.table.setHorizontalHeaderLabels(["Nome", "Nome PJ", "Especialização", "Status", "Ação"])
        self.layout.addWidget(self.table)
        # Botões de ação
        btn_layout = QHBoxLayout()
        add_btn = PrimaryButton("Adicionar Médico")
        add_btn.setIcon(get_icon("add"))
        add_btn.clicked.connect(self.adicionar_medico)
        btn_layout.addWidget(add_btn)
        export_csv_btn = PrimaryButton("Exportar CSV")
        export_csv_btn.setIcon(get_icon("download"))
        export_csv_btn.clicked.connect(self.exportar_csv)
        btn_layout.addWidget(export_csv_btn)
        import_csv_btn = PrimaryButton("Importar CSV")
        import_csv_btn.setIcon(get_icon("upload"))
        import_csv_btn.clicked.connect(self.importar_csv)
        btn_layout.addWidget(import_csv_btn)
        self.layout.addLayout(btn_layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        self._especializacoes = {e.id: e.nome for e in get_especializacoes()}
        self._medicos = get_medicos()
        for medico in self._medicos:
            self.add_row(medico)

    def add_row(self, medico):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(medico.nome))
        self.table.setItem(row, 1, QTableWidgetItem(medico.nome_pj or ""))
        especializacao_nome = self._especializacoes.get(medico.especializacao_id, "-")
        self.table.setItem(row, 2, QTableWidgetItem(especializacao_nome))
        self.table.setItem(row, 3, QTableWidgetItem(str(medico.status)))
        # Coluna ação: editar e excluir juntos (SVG igual Especializações)
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
        btn_edit.setIconSize(btn_edit.size() - QSize(8, 8))
        btn_edit.setStyleSheet('background-color: #FFD600; color: black; border-radius: 6px;')
        btn_edit.clicked.connect(lambda _, m=medico: self.editar_medico(m))
        btn_del = QPushButton()
        btn_del.setIcon(del_icon)
        btn_del.setToolTip('Excluir')
        btn_del.setFixedSize(28, 28)
        btn_del.setIconSize(btn_del.size() - QSize(8, 8))
        btn_del.setStyleSheet('background-color: #d32f2f; color: white; border-radius: 6px;')
        btn_del.clicked.connect(lambda _, m=medico: self.excluir_medico_dialog(m))
        action_layout.addWidget(btn_edit)
        action_layout.addWidget(btn_del)
        action_layout.addStretch()
        self.table.setCellWidget(row, 4, action_widget)

    def buscar_medico(self):
        termo = self.search_input.text().strip().upper()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                visivel = termo in item.text().upper()
                self.table.setRowHidden(row, not visivel)
        if not termo:
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)

    def adicionar_medico(self):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox
        class UpperLineEdit(QLineEdit):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.textChanged.connect(self.to_upper)
            def to_upper(self, text):
                cursor_pos = self.cursorPosition()
                self.setText(text.upper())
                self.setCursorPosition(cursor_pos)
        class AddDialog(QDialog):
            def __init__(self, parent=None, especializacoes=None):
                super().__init__(parent)
                self.setWindowTitle('Adicionar Médico')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input_nome = UpperLineEdit()
                self.input_nome.setPlaceholderText('NOME DO MÉDICO')
                layout.addWidget(QLabel('Nome do médico:'))
                layout.addWidget(self.input_nome)
                self.input_pj = UpperLineEdit()
                self.input_pj.setPlaceholderText('NOME DA PESSOA JURÍDICA (opcional)')
                layout.addWidget(QLabel('Nome PJ:'))
                layout.addWidget(self.input_pj)
                self.combo_especializacao = QComboBox()
                self.especializacoes = especializacoes or []
                for esp in self.especializacoes:
                    self.combo_especializacao.addItem(esp.nome, esp.id)
                layout.addWidget(QLabel('Especialização:'))
                layout.addWidget(self.combo_especializacao)
                self.combo_status = QComboBox()
                self.combo_status.addItems(['ativo', 'inativo', 'afastado'])
                layout.addWidget(QLabel('Status:'))
                layout.addWidget(self.combo_status)
                btn_layout = QHBoxLayout()
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
        especializacoes = get_especializacoes()
        dialog = AddDialog(self, especializacoes)
        if dialog.exec_() == QDialog.Accepted and dialog.input_nome.text().strip():
            nome = dialog.input_nome.text().strip()
            nome_pj = dialog.input_pj.text().strip()
            especializacao_id = dialog.combo_especializacao.currentData()
            status = dialog.combo_status.currentText()
            # Obter user_id do usuário logado
            user_id = getattr(self.parent(), 'usuario', None)
            if user_id and hasattr(user_id, 'id'):
                user_id = user_id.id
            elif hasattr(self, 'usuario') and hasattr(self.usuario, 'id'):
                user_id = self.usuario.id
            else:
                user_id = 1  # fallback para admin
            create_medico(nome, nome_pj, especializacao_id, status, user_id)
            self.load_data()
            MessageManager.info(self, "Cadastro", "Médico adicionado com sucesso.")

    def excluir_medico_dialog(self, medico):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
        class ConfirmDialog(QDialog):
            def __init__(self, parent=None, nome=""):
                super().__init__(parent)
                self.setWindowTitle('Confirmação')
                self.setModal(True)
                layout = QVBoxLayout()
                label = QLabel(f"Deseja excluir o médico '{nome}'?")
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
        dialog = ConfirmDialog(self, medico.nome)
        if dialog.exec_() == QDialog.Accepted:
            self.excluir_medico(medico.id)

    def excluir_medico(self, medico_id: int):
        if self.perfil != 'admin':
            MessageManager.error(self, "Acesso negado", "Você não tem permissão para excluir médicos.")
            return
        if self.integrity_checker and not self.integrity_checker.can_delete_medico(medico_id):
            MessageManager.error(self, "Exclusão não permitida", "Este médico possui escalas vinculadas e não pode ser excluído.")
            return
        user_id = getattr(self.parent(), 'usuario', None)
        if user_id and hasattr(user_id, 'id'):
            user_id = user_id.id
        elif hasattr(self, 'usuario') and hasattr(self.usuario, 'id'):
            user_id = self.usuario.id
        else:
            user_id = 1  # fallback para admin
        delete_medico(medico_id, user_id)
        log_action(self.perfil, 'delete', 'medico', medico_id)
        self.load_data()
        MessageManager.info(self, "Exclusão", "Médico excluído com sucesso.")

    def exportar_csv(self):
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            linha = [self.table.item(row, col).text() if self.table.item(row, col) else '' for col in range(self.table.columnCount())]
            data.append(linha)
        if export_to_csv(self, headers, data):
            MessageManager.info(self, "Exportação", "Médicos exportados com sucesso.")

    def importar_csv(self):
        rows = import_from_csv(self)
        if not rows:
            return
        import_ok = True
        for row in rows[1:]:
            if not all(row):
                MessageManager.error(self, "Importação", "Dados incompletos na linha: {}".format(row))
                import_ok = False
                continue
            if self.integrity_checker and not self.integrity_checker.can_delete_especializacao(row[1]):
                MessageManager.error(self, "Importação", f"Especialização inválida para médico: {row[0]}")
                import_ok = False
                continue
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for col, value in enumerate(row):
                self.table.setItem(row_idx, col, QTableWidgetItem(value))
        if import_ok:
            MessageManager.info(self, "Importação", "Médicos importados com sucesso.")
            log_action(self.perfil, 'import', 'medico', details='importação em lote', result='sucesso')
        else:
            log_action(self.perfil, 'import', 'medico', details='importação com erros', result='erro')

    def editar_medico(self, medico):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox
        class UpperLineEdit(QLineEdit):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.textChanged.connect(self.to_upper)
            def to_upper(self, text):
                cursor_pos = self.cursorPosition()
                self.setText(text.upper())
                self.setCursorPosition(cursor_pos)
        class EditDialog(QDialog):
            def __init__(self, parent=None, medico=None, especializacoes=None):
                super().__init__(parent)
                self.setWindowTitle('Editar Médico')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input_nome = UpperLineEdit()
                self.input_nome.setText(medico.nome)
                layout.addWidget(QLabel('Nome do médico:'))
                layout.addWidget(self.input_nome)
                self.input_pj = UpperLineEdit()
                self.input_pj.setText(medico.nome_pj or "")
                layout.addWidget(QLabel('Nome PJ:'))
                layout.addWidget(self.input_pj)
                self.combo_especializacao = QComboBox()
                self.especializacoes = especializacoes or []
                idx_esp = 0
                for idx, esp in enumerate(self.especializacoes):
                    self.combo_especializacao.addItem(esp.nome, esp.id)
                    if esp.id == medico.especializacao_id:
                        idx_esp = idx
                self.combo_especializacao.setCurrentIndex(idx_esp)
                layout.addWidget(QLabel('Especialização:'))
                layout.addWidget(self.combo_especializacao)
                self.combo_status = QComboBox()
                self.combo_status.addItems(['ativo', 'inativo', 'afastado'])
                status_idx = self.combo_status.findText(str(medico.status))
                if status_idx >= 0:
                    self.combo_status.setCurrentIndex(status_idx)
                layout.addWidget(QLabel('Status:'))
                layout.addWidget(self.combo_status)
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
        especializacoes = get_especializacoes()
        dialog = EditDialog(self, medico, especializacoes)
        if dialog.exec_() == QDialog.Accepted and dialog.input_nome.text().strip():
            nome = dialog.input_nome.text().strip()
            nome_pj = dialog.input_pj.text().strip()
            especializacao_id = dialog.combo_especializacao.currentData()
            status = dialog.combo_status.currentText()
            # Obter user_id do usuário logado
            user_id = getattr(self.parent(), 'usuario', None)
            if user_id and hasattr(user_id, 'id'):
                user_id = user_id.id
            elif hasattr(self, 'usuario') and hasattr(self.usuario, 'id'):
                user_id = self.usuario.id
            else:
                user_id = 1  # fallback para admin
            update_medico(medico.id, nome, nome_pj, especializacao_id, status, user_id)
            self.load_data()
            MessageManager.info(self, "Edição", "Médico editado com sucesso.")
