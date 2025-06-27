from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QComboBox, QDateEdit, QPushButton, QHBoxLayout, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt
from app.components.escalas_table import EscalasTable
from app.components.escalas_action_buttons import EscalasActionButtons
from app.components.notifier import Notifier
from app.core.escala_repository import EscalaRepository
from app.models.escala_plantonista import EscalaPlantonista
from app.models.medico import Medico, StatusMedicoEnum
from app.database import db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class PlantonistasView(QWidget):
    def __init__(self, parent=None, integrity_checker=None, perfil=None, db_session: Session = None):
        super().__init__(parent)
        self.setObjectName("plantonistas_view")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.integrity_checker = integrity_checker
        self.perfil = perfil
        self.db_session = db_session or db.session
        self.escala_repo = EscalaRepository(self.db_session)
        self.init_ui()

    def init_ui(self):
        title = QLabel("Gestão de Escalas de Plantonistas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(title)
        filter_widget = QWidget()
        filter_layout = QFormLayout()
        filter_layout.setLabelAlignment(Qt.AlignRight)
        filter_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        filter_layout.setHorizontalSpacing(18)
        filter_layout.setVerticalSpacing(8)
        self.ano_combo = QComboBox()
        self.ano_combo.setFixedWidth(110)
        self.ano_combo.currentIndexChanged.connect(self.atualizar_dias)
        self.ano_combo.currentIndexChanged.connect(self.buscar_escala)
        filter_layout.addRow(QLabel("Ano:"), self.ano_combo)
        self.mes_combo = QComboBox()
        self.mes_combo.setFixedWidth(130)
        self.mes_combo.currentIndexChanged.connect(self.atualizar_dias)
        self.mes_combo.currentIndexChanged.connect(self.buscar_escala)
        filter_layout.addRow(QLabel("Mês:"), self.mes_combo)
        self.dia_combo = QComboBox()
        self.dia_combo.setFixedWidth(90)
        self.dia_combo.currentIndexChanged.connect(self.buscar_escala)
        filter_layout.addRow(QLabel("Dia:"), self.dia_combo)
        self.medico_combo = QComboBox()
        self.medico_combo.setFixedWidth(220)
        self.popular_medicos()
        self.medico_combo.currentIndexChanged.connect(self.buscar_escala)
        filter_layout.addRow(QLabel("Médico:"), self.medico_combo)
        filter_widget.setLayout(filter_layout)
        self.layout.addWidget(filter_widget)
        self.layout.addSpacing(8)
        self.table_widget = EscalasTable(on_edit=self.editar_escala, on_delete=self.excluir_escala_dialog)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.get_table().horizontalHeader().setStretchLastSection(True)
        self.table_widget.get_table().horizontalHeader().setSectionResizeMode(1)
        self.layout.addWidget(self.table_widget, stretch=1)
        self.action_buttons = EscalasActionButtons(
            on_add=self.adicionar_escala,
            on_export=self.exportar_csv,
            on_import=self.importar_csv,
            on_print=self.imprimir_relatorio
        )
        self.layout.addWidget(self.action_buttons)
        self.load_data()
        self.popular_ano_mes()

    def popular_ano_mes(self):
        anos = [str(ano) for ano in range(2019, 2031)]
        self.ano_combo.clear()
        self.ano_combo.addItem("Todos os anos", None)
        self.ano_combo.addItems(anos)
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        self.mes_combo.clear()
        self.mes_combo.addItem("Todos os meses", None)
        self.mes_combo.addItems(meses)
        self.dia_combo.clear()
        self.dia_combo.addItem("Todos os dias", None)
        # Seleciona o mês atual
        from datetime import datetime
        mes_atual = datetime.now().month
        self.mes_combo.setCurrentIndex(mes_atual)  # +1 por causa do item "Todos os meses"
        self.ano_combo.setCurrentText(str(datetime.now().year))

    def atualizar_dias(self):
        self.dia_combo.clear()
        self.dia_combo.addItem("Todos os dias", None)
        ano = self.ano_combo.currentText()
        mes = self.mes_combo.currentIndex() if self.mes_combo.currentIndex() > 0 else None
        if ano and ano != "Todos os anos" and mes:
            try:
                ano = int(ano)
                if mes == 2:
                    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
                        ultimo_dia = 29
                    else:
                        ultimo_dia = 28
                elif mes in [4, 6, 9, 11]:
                    ultimo_dia = 30
                else:
                    ultimo_dia = 31
                dias = [str(dia).zfill(2) for dia in range(1, ultimo_dia + 1)]
                self.dia_combo.addItems(dias)
            except Exception:
                pass

    def load_data(self):
        escalas = self.escala_repo.get_all()
        dados = []
        for escala in escalas:
            try:
                data_fmt = escala.data.strftime('%d/%m/%Y')
            except Exception:
                data_fmt = str(escala.data)
            dados.append({
                "id": escala.id,
                "data": data_fmt,
                "turno": getattr(escala, 'turno', '').upper(),
                "medico0": escala.medico1.nome.upper() if hasattr(escala, 'medico1') and escala.medico1 else '',
                "medico1": escala.medico2.nome.upper() if hasattr(escala, 'medico2') and escala.medico2 else ''
            })
        self.table_widget.set_data(dados)

    def popular_medicos(self):
        self.medico_combo.clear()
        self.medico_combo.addItem("Todos os médicos", None)
        medicos_ativos = self.db_session.query(Medico).filter(Medico.status == StatusMedicoEnum.ATIVO.value).all()
        for medico in medicos_ativos:
            self.medico_combo.addItem(medico.nome, medico.id)

    def buscar_escala(self):
        ano = self.ano_combo.currentText()
        mes = self.mes_combo.currentIndex() if self.mes_combo.currentIndex() > 0 else None
        dia = self.dia_combo.currentText()
        medico_id = self.medico_combo.currentData()
        escalas = self.escala_repo.get_all()
        if ano and ano != "Todos os anos":
            escalas = [e for e in escalas if e.data.year == int(ano)]
        if mes:
            escalas = [e for e in escalas if e.data.month == mes]
        if dia and dia != "Todos os dias":
            escalas = [e for e in escalas if e.data.day == int(dia)]
        if medico_id:
            escalas = [e for e in escalas if (getattr(e, 'medico1_id', None) == medico_id) or (getattr(e, 'medico2_id', None) == medico_id)]
        dados = []
        for escala in escalas:
            dados.append({
                "id": escala.id,
                "data": escala.data.strftime('%d/%m/%Y'),
                "turno": getattr(escala, 'turno', ''),
                "medico0": escala.medico1.nome if hasattr(escala, 'medico1') and escala.medico1 else '',
                "medico1": escala.medico2.nome if hasattr(escala, 'medico2') and escala.medico2 else ''
            })
        self.table_widget.set_data(dados)

    def adicionar_escala(self):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QDateEdit
        from PyQt5.QtCore import QDate
        from datetime import datetime
        class EscalaDialog(QDialog):
            def __init__(self, parent=None, medicos_ativos=None):
                super().__init__(parent)
                self.setWindowTitle('Adicionar Escala')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input_data = QDateEdit()
                self.input_data.setDisplayFormat('dd/MM/yyyy')
                self.input_data.setCalendarPopup(True)
                self.input_data.setDate(QDate.currentDate())
                layout.addWidget(QLabel('Data:'))
                layout.addWidget(self.input_data)
                self.input_turno = QComboBox()
                self.input_turno.addItems(['DIURNO', 'NOTURNO'])
                layout.addWidget(QLabel('Turno:'))
                layout.addWidget(self.input_turno)
                self.input_medico0 = QComboBox()
                self.input_medico1 = QComboBox()
                medicos_ativos = medicos_ativos or []
                for m in medicos_ativos:
                    self.input_medico0.addItem(m.nome.upper(), m.id)
                    self.input_medico1.addItem(m.nome.upper(), m.id)
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
        medicos_ativos = self.db_session.query(Medico).filter(Medico.status == StatusMedicoEnum.ATIVO.value).all()
        dialog = EscalaDialog(self, medicos_ativos=medicos_ativos)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.input_data.date().toPyDate()
                turno = dialog.input_turno.currentText().upper()
                medico1_id = dialog.input_medico0.currentData()
                medico2_id = dialog.input_medico1.currentData()
                if not data or medico1_id is None or medico2_id is None:
                    Notifier.warning(self, "Campos obrigatórios", "Preencha todos os campos. Caso não veja os botões de ação, feche e reabra a tela.")
                    return
                if medico1_id == medico2_id:
                    Notifier.warning(self, "Médicos iguais", "Selecione médicos diferentes para a escala. Caso não veja os botões de ação, feche e reabra a tela.")
                    return
                existe = self.db_session.query(EscalaPlantonista).filter_by(data=data, turno=turno).first()
                if existe:
                    Notifier.warning(self, "Duplicidade", f"Já existe escala para {data.strftime('%d/%m/%Y')} - {turno}. Caso não veja os botões de ação, feche e reabra a tela.")
                    return
                nova_escala = EscalaPlantonista(data=data, turno=turno, medico1_id=medico1_id, medico2_id=medico2_id)
                self.escala_repo.create(nova_escala, user_id=1)
                self.load_data()
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(None, "Sucesso", "Escala adicionada com sucesso. Caso não veja os botões de ação, feche e reabra a tela.")
            except Exception as e:
                Notifier.error(self, "Erro", str(e))

    def editar_escala(self, escala):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QDateEdit
        from PyQt5.QtCore import QDate
        from datetime import datetime
        class EscalaDialog(QDialog):
            def __init__(self, parent=None, escala=None, medicos_ativos=None):
                super().__init__(parent)
                self.setWindowTitle('Editar Escala')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input_data = QDateEdit()
                self.input_data.setDisplayFormat('dd/MM/yyyy')
                self.input_data.setCalendarPopup(True)
                if escala:
                    try:
                        data_fmt = datetime.strptime(escala['data'], '%d/%m/%Y')
                        self.input_data.setDate(QDate(data_fmt.year, data_fmt.month, data_fmt.day))
                    except Exception:
                        self.input_data.setDate(QDate.currentDate())
                else:
                    self.input_data.setDate(QDate.currentDate())
                layout.addWidget(QLabel('Data:'))
                layout.addWidget(self.input_data)
                self.input_turno = QComboBox()
                self.input_turno.addItems(['DIURNO', 'NOTURNO'])
                layout.addWidget(QLabel('Turno:'))
                layout.addWidget(self.input_turno)
                self.input_medico0 = QComboBox()
                self.input_medico1 = QComboBox()
                medicos_ativos = medicos_ativos or []
                for m in medicos_ativos:
                    self.input_medico0.addItem(m.nome.upper(), m.id)
                    self.input_medico1.addItem(m.nome.upper(), m.id)
                layout.addWidget(QLabel('Médico 0:'))
                layout.addWidget(self.input_medico0)
                layout.addWidget(QLabel('Médico 1:'))
                layout.addWidget(self.input_medico1)
                if escala:
                    idx = self.input_turno.findText(escala['turno'].upper())
                    if idx >= 0:
                        self.input_turno.setCurrentIndex(idx)
                    idx0 = self.input_medico0.findText(escala['medico0'].upper())
                    if idx0 >= 0:
                        self.input_medico0.setCurrentIndex(idx0)
                    idx1 = self.input_medico1.findText(escala['medico1'].upper())
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
        medicos_ativos = self.db_session.query(Medico).filter(Medico.status == StatusMedicoEnum.ATIVO.value).all()
        dialog = EscalaDialog(self, escala, medicos_ativos=medicos_ativos)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.input_data.date().toPyDate()
                turno = dialog.input_turno.currentText().upper()
                medico1_id = dialog.input_medico0.currentData()
                medico2_id = dialog.input_medico1.currentData()
                existe = self.db_session.query(EscalaPlantonista).filter(
                    EscalaPlantonista.data == data,
                    EscalaPlantonista.turno == turno,
                    EscalaPlantonista.id != escala['id']
                ).first()
                if existe:
                    Notifier.error(self, "Duplicidade", f"Já existe escala para {data.strftime('%d/%m/%Y')} - {turno}.")
                    return
                escala_obj = self.escala_repo.get_by_id(escala['id'])
                if not escala_obj:
                    Notifier.error(self, "Erro", "Escala não encontrada.")
                    return
                escala_obj.data = data
                escala_obj.turno = turno
                escala_obj.medico1_id = medico1_id
                escala_obj.medico2_id = medico2_id
                self.escala_repo.update(escala_obj, user_id=1)
                self.load_data()
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(None, "Sucesso", "Escala editada com sucesso.")
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

    def imprimir_relatorio(self):
        table = self.table_widget.get_table()
        cabecalhos = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
        dados = []
        for row in range(table.rowCount()):
            if table.isRowHidden(row):
                continue
            linha = [table.item(row, col).text() if table.item(row, col) else '' for col in range(table.columnCount())]
            dados.append(linha)
        nome_arquivo = os.path.expanduser("~\\relatorio_escalas.pdf")
        gerar_pdf_relatorio(nome_arquivo, "Relatório de Escalas", cabecalhos, dados, rodape="GEM - Sistema de Escalas Médicas")
        Notifier.info(self, "Impressão", f"Relatório gerado em {nome_arquivo}")

    def exportar_csv(self):
        table = self.table_widget.get_table()
        headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
        data = []
        for row in range(table.rowCount()):
            linha = [table.item(row, col).text() if table.item(row, col) else '' for col in range(table.columnCount())]
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
            for i in range(self.table_widget.get_table().rowCount()):
                if self.table_widget.get_table().item(i, 0) and self.table_widget.get_table().item(i, 0).text() == row[0] and self.table_widget.get_table().item(i, 1) and self.table_widget.get_table().item(i, 1).text() == row[1]:
                    Notifier.error(self, "Importação", f"Escala já existe para data/turno: {row[0]} {row[1]}")
                    import_ok = False
                    break
            else:
                row_idx = self.table_widget.get_table().rowCount()
                self.table_widget.get_table().insertRow(row_idx)
                for col, value in enumerate(row):
                    self.table_widget.get_table().setItem(row_idx, col, QTableWidgetItem(value))
        if import_ok:
            Notifier.info(self, "Importação", "Escalas importadas com sucesso.")
            log_action(self.perfil, 'import', 'escala', details='importação em lote', result='sucesso')
        else:
            log_action(self.perfil, 'import', 'escala', details='importação com erros', result='erro')