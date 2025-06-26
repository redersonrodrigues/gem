"""
Tela de gestão de escalas - PyQt5
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QDialog, QLineEdit, QComboBox
from app.components.ui_elements import PrimaryButton, SearchField, StyledTable
from app.components.notifier import Notifier
from app.components.icon_helper import get_icon
from app.utils.integrity_checker import IntegrityChecker
from app.components.print_helper import gerar_pdf_relatorio
from app.utils.data_io import export_to_csv, import_from_csv, export_to_json, import_from_json
from app.components.ui_logger import log_action
from app.core.escala_repository import EscalaRepository
from app.models.escala_plantonista import EscalaPlantonista
from app.models.medico import Medico, StatusMedicoEnum
from app.database import db
from sqlalchemy.orm import Session
from datetime import datetime
import os

class EscalasView(QWidget):
    def __init__(self, parent=None, integrity_checker: IntegrityChecker = None, perfil=None, tipo=None, db_session: Session = None):
        super().__init__(parent)
        self.setObjectName("escalas_view")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.integrity_checker = integrity_checker
        self.perfil = perfil
        self.tipo = tipo  # Novo argumento para diferenciar Plantonista/Sobreaviso
        self.db_session = db_session or db.session  # Usa sessão injetada ou padrão
        self.escala_repo = EscalaRepository(self.db_session)
        self.init_ui()

    def init_ui(self):
        titulo = "Gestão de Escalas"
        if self.tipo == 'Plantonista':
            titulo = "Gestão de Escalas de Plantonistas"
        elif self.tipo == 'Sobreaviso':
            titulo = "Gestão de Escalas de Sobreaviso"
        title = QLabel(titulo)
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
        # Tabela de escalas (agora com coluna Ação)
        self.table = StyledTable(0, 5)
        self.table.setHorizontalHeaderLabels(["Data", "Turno", "Médico 0", "Médico 1", "Ação"])
        self.layout.addWidget(self.table)
        # Botões de ação
        btn_layout = QHBoxLayout()
        add_btn = PrimaryButton("Adicionar Escala")
        add_btn.setIcon(get_icon("add"))
        add_btn.clicked.connect(self.adicionar_escala)
        btn_layout.addWidget(add_btn)
        export_csv_btn = PrimaryButton("Exportar CSV")
        export_csv_btn.setIcon(get_icon("download"))
        export_csv_btn.clicked.connect(self.exportar_csv)
        btn_layout.addWidget(export_csv_btn)
        import_csv_btn = PrimaryButton("Importar CSV")
        import_csv_btn.setIcon(get_icon("upload"))
        import_csv_btn.clicked.connect(self.importar_csv)
        btn_layout.addWidget(import_csv_btn)
        print_btn = PrimaryButton("Imprimir Relatório")
        print_btn.setIcon(get_icon("calendar"))
        print_btn.clicked.connect(self.imprimir_relatorio)
        btn_layout.addWidget(print_btn)
        self.layout.addLayout(btn_layout)
        # Carregar dados (mock)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        escalas = self.escala_repo.get_all()
        for escala in escalas:
            self.add_row({
                "id": escala.id,
                "data": escala.data.strftime('%Y-%m-%d'),
                "turno": getattr(escala, 'turno', ''),
                "medico0": escala.medico1.nome if hasattr(escala, 'medico1') and escala.medico1 else '',
                "medico1": escala.medico2.nome if hasattr(escala, 'medico2') and escala.medico2 else ''
            })

    def add_row(self, escala):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(escala["data"]))
        self.table.setItem(row, 1, QTableWidgetItem(escala["turno"]))
        self.table.setItem(row, 2, QTableWidgetItem(escala["medico0"]))
        self.table.setItem(row, 3, QTableWidgetItem(escala["medico1"]))
        # Coluna ação: editar/excluir
        pen_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'static', 'icons', 'solid', 'pen.svg'))
        trash_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'static', 'icons', 'solid', 'trash.svg'))
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
        btn_edit.setStyleSheet('background-color: #FFD600; color: black; border-radius: 6px;')
        btn_edit.clicked.connect(lambda _, e=escala: self.editar_escala(e))
        btn_del = QPushButton()
        btn_del.setIcon(del_icon)
        btn_del.setToolTip('Excluir')
        btn_del.setFixedSize(28, 28)
        btn_del.setStyleSheet('background-color: #d32f2f; color: white; border-radius: 6px;')
        btn_del.clicked.connect(lambda _, e=escala: self.excluir_escala_dialog(e))
        action_layout.addWidget(btn_edit)
        action_layout.addWidget(btn_del)
        action_layout.addStretch()
        self.table.setCellWidget(row, 4, action_widget)

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
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton
        class EscalaDialog(QDialog):
            def __init__(self, parent=None, escala=None, medicos_ativos=None):
                super().__init__(parent)
                self.setWindowTitle('Adicionar Escala' if escala is None else 'Editar Escala')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input_data = QLineEdit()
                self.input_data.setPlaceholderText('AAAA-MM-DD')
                layout.addWidget(QLabel('Data:'))
                layout.addWidget(self.input_data)
                self.input_turno = QComboBox()
                self.input_turno.addItems(['Manhã', 'Tarde', 'Noite'])
                layout.addWidget(QLabel('Turno:'))
                layout.addWidget(self.input_turno)
                self.input_medico0 = QComboBox()
                self.input_medico1 = QComboBox()
                medicos_ativos = medicos_ativos or []
                for m in medicos_ativos:
                    self.input_medico0.addItem(m.nome, m.id)
                    self.input_medico1.addItem(m.nome, m.id)
                layout.addWidget(QLabel('Médico 0:'))
                layout.addWidget(self.input_medico0)
                layout.addWidget(QLabel('Médico 1:'))
                layout.addWidget(self.input_medico1)
                btn_layout = QHBoxLayout()
                btn_ok = QPushButton('Confirmar')
                btn_cancel = QPushButton('Cancelar')
                btn_ok.setStyleSheet('background-color: #388e3c; color: white; font-weight: bold;')
                btn_cancel.setStyleSheet('background-color: #d32f2f; color: white; font-weight: bold;')
                btn_ok.clicked.connect(self.accept)
                btn_cancel.clicked.connect(self.reject)
                btn_layout.addWidget(btn_ok)
                btn_layout.addWidget(btn_cancel)
                layout.addLayout(btn_layout)
                self.setLayout(layout)
        # Buscar médicos ativos
        medicos_ativos = self.db_session.query(Medico).filter(Medico.status == StatusMedicoEnum.ATIVO.value).all()
        dialog = EscalaDialog(self, medicos_ativos=medicos_ativos)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.input_data.text().strip()
                turno = dialog.input_turno.currentText()
                medico1_id = dialog.input_medico0.currentData()
                medico2_id = dialog.input_medico1.currentData()
                # Validação de data
                data_dt = datetime.strptime(data, '%Y-%m-%d').date()
                # Checar duplicidade data/turno
                existe = self.db_session.query(EscalaPlantonista).filter_by(data=data_dt, turno=turno).first()
                if existe:
                    Notifier.error(self, "Duplicidade", f"Já existe escala para {data} - {turno}.")
                    return
                nova_escala = EscalaPlantonista(data=data_dt, turno=turno, medico1_id=medico1_id, medico2_id=medico2_id)
                self.escala_repo.create(nova_escala, user_id=1)
                self.load_data()
                Notifier.info(self, "Sucesso", "Escala adicionada com sucesso.")
            except Exception as e:
                Notifier.error(self, "Erro", str(e))

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

    def editar_escala(self, escala):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
        class EscalaDialog(QDialog):
            def __init__(self, parent=None, escala=None, medicos_ativos=None):
                super().__init__(parent)
                self.setWindowTitle('Editar Escala')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input_data = QLineEdit()
                self.input_data.setPlaceholderText('AAAA-MM-DD')
                layout.addWidget(QLabel('Data:'))
                layout.addWidget(self.input_data)
                self.input_turno = QComboBox()
                self.input_turno.addItems(['Manhã', 'Tarde', 'Noite'])
                layout.addWidget(QLabel('Turno:'))
                layout.addWidget(self.input_turno)
                self.input_medico0 = QComboBox()
                self.input_medico1 = QComboBox()
                medicos_ativos = medicos_ativos or []
                for m in medicos_ativos:
                    self.input_medico0.addItem(m.nome, m.id)
                    self.input_medico1.addItem(m.nome, m.id)
                layout.addWidget(QLabel('Médico 0:'))
                layout.addWidget(self.input_medico0)
                layout.addWidget(QLabel('Médico 1:'))
                layout.addWidget(self.input_medico1)
                if escala:
                    self.input_data.setText(escala['data'])
                    idx = self.input_turno.findText(escala['turno'])
                    if idx >= 0:
                        self.input_turno.setCurrentIndex(idx)
                    # Seleciona médicos atuais
                    idx0 = self.input_medico0.findText(escala['medico0'])
                    if idx0 >= 0:
                        self.input_medico0.setCurrentIndex(idx0)
                    idx1 = self.input_medico1.findText(escala['medico1'])
                    if idx1 >= 0:
                        self.input_medico1.setCurrentIndex(idx1)
                btn_layout = QHBoxLayout()
                btn_ok = QPushButton('Confirmar')
                btn_cancel = QPushButton('Cancelar')
                btn_ok.setStyleSheet('background-color: #388e3c; color: white; font-weight: bold;')
                btn_cancel.setStyleSheet('background-color: #d32f2f; color: white; font-weight: bold;')
                btn_ok.clicked.connect(self.accept)
                btn_cancel.clicked.connect(self.reject)
                btn_layout.addWidget(btn_ok)
                btn_layout.addWidget(btn_cancel)
                layout.addLayout(btn_layout)
                self.setLayout(layout)
        # Buscar médicos ativos
        medicos_ativos = self.db_session.query(Medico).filter(Medico.status == StatusMedicoEnum.ATIVO.value).all()
        dialog = EscalaDialog(self, escala, medicos_ativos=medicos_ativos)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.input_data.text().strip()
                turno = dialog.input_turno.currentText()
                medico1_id = dialog.input_medico0.currentData()
                medico2_id = dialog.input_medico1.currentData()
                data_dt = datetime.strptime(data, '%Y-%m-%d').date()
                # Checar duplicidade data/turno (exceto a própria escala)
                existe = self.db_session.query(EscalaPlantonista).filter(
                    EscalaPlantonista.data == data_dt,
                    EscalaPlantonista.turno == turno,
                    EscalaPlantonista.id != escala['id']
                ).first()
                if existe:
                    Notifier.error(self, "Duplicidade", f"Já existe escala para {data} - {turno}.")
                    return
                escala_obj = self.escala_repo.get_by_id(escala['id'])
                if not escala_obj:
                    Notifier.error(self, "Erro", "Escala não encontrada.")
                    return
                escala_obj.data = data_dt
                escala_obj.turno = turno
                escala_obj.medico1_id = medico1_id
                escala_obj.medico2_id = medico2_id
                self.escala_repo.update(escala_obj, user_id=1)
                self.load_data()
                Notifier.info(self, "Sucesso", "Escala editada com sucesso.")
            except Exception as e:
                Notifier.error(self, "Erro", str(e))

    def excluir_escala_dialog(self, escala):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
        class ConfirmDialog(QDialog):
            def __init__(self, parent=None, data="", turno=""):
                super().__init__(parent)
                self.setWindowTitle('Confirmação')
                self.setModal(True)
                layout = QVBoxLayout()
                label = QLabel(f"Deseja excluir a escala do dia '{data}' turno '{turno}'?")
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
        dialog = ConfirmDialog(self, escala["data"], escala["turno"])
        if dialog.exec_() == QDialog.Accepted:
            self.excluir_escala(escala["id"])

    def excluir_escala(self, escala_id: int):
        if self.perfil != 'admin':
            Notifier.error(self, "Acesso negado", "Você não tem permissão para excluir escalas.")
            return
        if self.integrity_checker and not self.integrity_checker.can_delete_escala(escala_id):
            Notifier.error(self, "Exclusão não permitida", "Esta escala não pode ser excluída devido a vínculos.")
            return
        escala = self.escala_repo.get_by_id(escala_id)
        if not escala:
            Notifier.error(self, "Erro", "Escala não encontrada.")
            return
        try:
            self.escala_repo.delete(escala, user_id=1)
            self.load_data()
            Notifier.info(self, "Exclusão", "Escala excluída com sucesso.")
        except Exception as e:
            Notifier.error(self, "Erro", str(e))
