from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QComboBox, QDateEdit, QPushButton, QHBoxLayout, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt
from app.components.escalas_table import EscalasTable
from app.components.escalas_action_buttons import EscalasActionButtons
from app.components.notifier import Notifier
from app.core.escala_repository import EscalaRepository
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico, StatusMedicoEnum
from app.models.especializacao import Especializacao
from app.database import db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class SobreavisosView(QWidget):
    def __init__(self, parent=None, integrity_checker=None, perfil=None, db_session: Session = None):
        super().__init__(parent)
        self.setObjectName("sobreavisos_view")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.integrity_checker = integrity_checker
        self.perfil = perfil
        self.db_session = db_session or db.session
        self.escala_repo = EscalaRepository(self.db_session)
        self.init_ui()

    def init_ui(self):
        title = QLabel("Gestão de Escalas de Sobreaviso")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(title)

        # Filtros
        filtros_layout = QFormLayout()
        self.especialidade_combo = QComboBox()
        self.especialidade_combo.addItem("Todas as Especialidades")
        # ...adicionar especialidades disponíveis...
        filtros_layout.addRow("Especialidade:", self.especialidade_combo)

        self.data_inicio = QDateEdit(calendarPopup=True)
        self.data_inicio.setDate(datetime.now())
        filtros_layout.addRow("Data Início:", self.data_inicio)

        self.data_fim = QDateEdit(calendarPopup=True)
        self.data_fim.setDate(datetime.now() + timedelta(days=6))
        filtros_layout.addRow("Data Fim:", self.data_fim)

        self.layout.addLayout(filtros_layout)

        # Tabela de Escalas
        self.tabela_escalas = EscalasTable()
        self.layout.addWidget(self.tabela_escalas)

        # Botões de Ação
        self.botoes_acao = EscalasActionButtons()
        self.layout.addWidget(self.botoes_acao)

        # Conectar sinais e slots
        self.botoes_acao.filtrar_btn.clicked.connect(self.filtrar_escalas)
        self.botoes_acao.limpar_btn.clicked.connect(self.limpar_filtros)
        # ...conexões adicionais conforme necessário...

    def popular_especialidades(self):
        self.especialidade_combo.clear()
        self.especialidade_combo.addItem("Todas as Especialidades", None)
        especialidades = self.db_session.query(Especializacao).all()
        for esp in especialidades:
            self.especialidade_combo.addItem(esp.nome, esp.id)

    def load_data(self):
        escalas = self.escala_repo.get_all_sobreaviso()
        dados = []
        for escala in escalas:
            try:
                data_ini_fmt = escala.data_inicial.strftime('%d/%m/%Y')
                data_fim_fmt = escala.data_final.strftime('%d/%m/%Y')
            except Exception:
                data_ini_fmt = str(escala.data_inicial)
                data_fim_fmt = str(escala.data_final)
            dados.append({
                "id": escala.id,
                "data_inicial": data_ini_fmt,
                "data_final": data_fim_fmt,
                "especialidade": escala.especializacao.nome if hasattr(escala, 'especializacao') and escala.especializacao else '',
                "medico": escala.medico1.nome if hasattr(escala, 'medico1') and escala.medico1 else ''
            })
        self.tabela_escalas.set_data(dados)

    def filtrar_escalas(self):
        especialidade_id = self.especialidade_combo.currentData()
        data_inicio = self.data_inicio.date().toPyDate()
        data_fim = self.data_fim.date().toPyDate()
        escalas = self.escala_repo.get_all_sobreaviso()
        if especialidade_id:
            escalas = [e for e in escalas if e.especializacao_id == especialidade_id]
        escalas = [e for e in escalas if e.data_inicial >= data_inicio and e.data_final <= data_fim]
        dados = []
        for escala in escalas:
            dados.append({
                "id": escala.id,
                "data_inicial": escala.data_inicial.strftime('%d/%m/%Y'),
                "data_final": escala.data_final.strftime('%d/%m/%Y'),
                "especialidade": escala.especializacao.nome if hasattr(escala, 'especializacao') and escala.especializacao else '',
                "medico": escala.medico1.nome if hasattr(escala, 'medico1') and escala.medico1 else ''
            })
        self.tabela_escalas.set_data(dados)

    def limpar_filtros(self):
        self.especialidade_combo.setCurrentIndex(0)
        self.data_inicio.setDate(datetime.now())
        self.data_fim.setDate(datetime.now() + timedelta(days=6))
        self.load_data()

    def adicionar_escala(self):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QDateEdit
        from PyQt5.QtCore import QDate
        class SobreavisoDialog(QDialog):
            def __init__(self, parent=None, especialidades=None, medicos=None):
                super().__init__(parent)
                self.setWindowTitle('Adicionar Escala de Sobreaviso')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input_especialidade = QComboBox()
                for esp in especialidades:
                    self.input_especialidade.addItem(esp.nome, esp.id)
                layout.addWidget(QLabel('Especialidade:'))
                layout.addWidget(self.input_especialidade)
                self.input_medico = QComboBox()
                for m in medicos:
                    self.input_medico.addItem(m.nome, m.id)
                layout.addWidget(QLabel('Médico:'))
                layout.addWidget(self.input_medico)
                self.input_data_inicial = QDateEdit()
                self.input_data_inicial.setDisplayFormat('dd/MM/yyyy')
                self.input_data_inicial.setCalendarPopup(True)
                self.input_data_inicial.setDate(QDate.currentDate())
                layout.addWidget(QLabel('Data Inicial:'))
                layout.addWidget(self.input_data_inicial)
                self.input_data_final = QDateEdit()
                self.input_data_final.setDisplayFormat('dd/MM/yyyy')
                self.input_data_final.setCalendarPopup(True)
                self.input_data_final.setDate(QDate.currentDate())
                layout.addWidget(QLabel('Data Final:'))
                layout.addWidget(self.input_data_final)
                btn_ok = QPushButton('Confirmar')
                btn_cancel = QPushButton('Cancelar')
                btn_ok.clicked.connect(self.accept)
                btn_cancel.clicked.connect(self.reject)
                layout.addWidget(btn_ok)
                layout.addWidget(btn_cancel)
                self.setLayout(layout)
        especialidades = self.db_session.query(Especializacao).all()
        medicos = self.db_session.query(Medico).filter(Medico.status == StatusMedicoEnum.ATIVO.value).all()
        dialog = SobreavisoDialog(self, especialidades, medicos)
        if dialog.exec_() == QDialog.Accepted:
            especialidade_id = dialog.input_especialidade.currentData()
            medico_id = dialog.input_medico.currentData()
            data_inicial = dialog.input_data_inicial.date().toPyDate()
            data_final = dialog.input_data_final.date().toPyDate()
            # Regras de negócio
            especialidade = self.db_session.query(Especializacao).get(especialidade_id)
            if especialidade.nome.upper() == 'ORTOPEDIA':
                # Quinzenal: 1-15 e 16-fim do mês
                if data_inicial.day == 1:
                    data_final = data_inicial.replace(day=15)
                else:
                    ultimo_dia = (data_inicial.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                    data_final = ultimo_dia
            else:
                # Semanal: pode começar antes e terminar depois, mas deve pertencer ao mês
                if data_inicial.month != data_final.month:
                    Notifier.warning(self, "Datas inválidas", "A escala deve pertencer ao mesmo mês.")
                    return
            nova_escala = EscalaSobreaviso(data_inicial=data_inicial, data_final=data_final, medico1_id=medico_id, especializacao_id=especialidade_id)
            self.escala_repo.create_sobreaviso(nova_escala, user_id=1)
            self.load_data()
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(None, "Sucesso", "Escala de sobreaviso adicionada com sucesso.")

    def editar_escala(self, escala):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QDateEdit
        from PyQt5.QtCore import QDate
        class SobreavisoDialog(QDialog):
            def __init__(self, parent=None, especialidades=None, medicos=None, escala=None):
                super().__init__(parent)
                self.setWindowTitle('Editar Escala de Sobreaviso')
                self.setModal(True)
                layout = QVBoxLayout()
                self.input_especialidade = QComboBox()
                for esp in especialidades:
                    self.input_especialidade.addItem(esp.nome, esp.id)
                layout.addWidget(QLabel('Especialidade:'))
                layout.addWidget(self.input_especialidade)
                self.input_medico = QComboBox()
                for m in medicos:
                    self.input_medico.addItem(m.nome, m.id)
                layout.addWidget(QLabel('Médico:'))
                layout.addWidget(self.input_medico)
                self.input_data_inicial = QDateEdit()
                self.input_data_inicial.setDisplayFormat('dd/MM/yyyy')
                self.input_data_inicial.setCalendarPopup(True)
                self.input_data_final = QDateEdit()
                self.input_data_final.setDisplayFormat('dd/MM/yyyy')
                self.input_data_final.setCalendarPopup(True)
                if escala:
                    self.input_especialidade.setCurrentText(escala['especialidade'])
                    self.input_medico.setCurrentText(escala['medico'])
                    data_ini = datetime.strptime(escala['data_inicial'], '%d/%m/%Y')
                    data_fim = datetime.strptime(escala['data_final'], '%d/%m/%Y')
                    self.input_data_inicial.setDate(QDate(data_ini.year, data_ini.month, data_ini.day))
                    self.input_data_final.setDate(QDate(data_fim.year, data_fim.month, data_fim.day))
                else:
                    self.input_data_inicial.setDate(QDate.currentDate())
                    self.input_data_final.setDate(QDate.currentDate())
                layout.addWidget(QLabel('Data Inicial:'))
                layout.addWidget(self.input_data_inicial)
                layout.addWidget(QLabel('Data Final:'))
                layout.addWidget(self.input_data_final)
                btn_ok = QPushButton('Confirmar')
                btn_cancel = QPushButton('Cancelar')
                btn_ok.clicked.connect(self.accept)
                btn_cancel.clicked.connect(self.reject)
                layout.addWidget(btn_ok)
                layout.addWidget(btn_cancel)
                self.setLayout(layout)
        especialidades = self.db_session.query(Especializacao).all()
        medicos = self.db_session.query(Medico).filter(Medico.status == StatusMedicoEnum.ATIVO.value).all()
        dialog = SobreavisoDialog(self, especialidades, medicos, escala)
        if dialog.exec_() == QDialog.Accepted:
            especialidade_id = dialog.input_especialidade.currentData()
            medico_id = dialog.input_medico.currentData()
            data_inicial = dialog.input_data_inicial.date().toPyDate()
            data_final = dialog.input_data_final.date().toPyDate()
            especialidade = self.db_session.query(Especializacao).get(especialidade_id)
            if especialidade.nome.upper() == 'ORTOPEDIA':
                if data_inicial.day == 1:
                    data_final = data_inicial.replace(day=15)
                else:
                    ultimo_dia = (data_inicial.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                    data_final = ultimo_dia
            else:
                if data_inicial.month != data_final.month:
                    Notifier.warning(self, "Datas inválidas", "A escala deve pertencer ao mesmo mês.")
                    return
            escala_obj = self.escala_repo.get_by_id_sobreaviso(escala['id'])
            if not escala_obj:
                Notifier.error(self, "Erro", "Escala não encontrada.")
                return
            escala_obj.data_inicial = data_inicial
            escala_obj.data_final = data_final
            escala_obj.medico1_id = medico_id
            escala_obj.especializacao_id = especialidade_id
            self.escala_repo.update_sobreaviso(escala_obj, user_id=1)
            self.load_data()
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(None, "Sucesso", "Escala de sobreaviso editada com sucesso.")

    def excluir_escala(self, escala_id):
        if self.perfil != 'admin':
            Notifier.error(self, "Acesso negado", "Você não tem permissão para excluir escalas.")
            return
        if self.integrity_checker and not self.integrity_checker.can_delete_escala(escala_id):
            Notifier.error(self, "Exclusão não permitida", "Esta escala não pode ser excluída devido a vínculos.")
            return
        escala = self.escala_repo.get_by_id_sobreaviso(escala_id)
        if not escala:
            Notifier.error(self, "Erro", "Escala não encontrada.")
            return
        try:
            self.escala_repo.delete_sobreaviso(escala, user_id=1)
            self.load_data()
            Notifier.info(self, "Exclusão", "Escala excluída com sucesso.")
        except Exception as e:
            Notifier.error(self, "Erro", str(e))

    def exportar_csv(self):
        table = self.tabela_escalas.get_table()
        headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
        data = []
        for row in range(table.rowCount()):
            linha = [table.item(row, col).text() if table.item(row, col) else '' for col in range(table.columnCount())]
            data.append(linha)
        if export_to_csv(self, headers, data):
            Notifier.info(self, "Exportação", "Escalas exportadas com sucesso.")

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
            row_idx = self.tabela_escalas.get_table().rowCount()
            self.tabela_escalas.get_table().insertRow(row_idx)
            for col, value in enumerate(row):
                self.tabela_escalas.get_table().setItem(row_idx, col, QTableWidgetItem(value))
        if import_ok:
            Notifier.info(self, "Importação", "Escalas importadas com sucesso.")
        else:
            Notifier.warning(self, "Importação", "Algumas linhas não foram importadas corretamente.")