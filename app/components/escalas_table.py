"""
Componente de tabela de escalas reutilizável para PyQt5
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidgetItem, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
from app.components.ui_elements import StyledTable

class EscalasTable(QWidget):
    def __init__(self, parent=None, on_edit=None, on_delete=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.table = StyledTable(0, 5)
        # Altera os nomes das colunas para Médico PS1 e Médico PS2
        self.table.setHorizontalHeaderLabels(["Data", "Turno", "Médico PS1", "Médico PS2", "Ação"])
        self.layout.addWidget(self.table)
        self.on_edit = on_edit
        self.on_delete = on_delete

    def clear(self):
        self.table.setRowCount(0)

    def set_data(self, escalas):
        self.clear()
        for escala in escalas:
            self.add_row(escala)

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
        edit_icon = QIcon(pen_path) if os.path.exists(pen_path) else QIcon()
        del_icon = QIcon(trash_path) if os.path.exists(trash_path) else QIcon()
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(6)
        action_layout.setAlignment(Qt.AlignCenter)  # Centraliza os botões
        btn_edit = QPushButton()
        btn_edit.setIcon(edit_icon)
        btn_edit.setToolTip('Editar')
        btn_edit.setFixedSize(28, 28)
        btn_edit.setStyleSheet('background-color: #FFD600; color: black; border-radius: 6px;')
        btn_edit.clicked.connect(lambda _, e=escala: self.on_edit(e) if self.on_edit else None)
        btn_del = QPushButton()
        btn_del.setIcon(del_icon)
        btn_del.setToolTip('Excluir')
        btn_del.setFixedSize(28, 28)
        btn_del.setStyleSheet('background-color: #d32f2f; color: white; border-radius: 6px;')
        btn_del.clicked.connect(lambda _, e=escala: self.on_delete(e) if self.on_delete else None)
        action_layout.addWidget(btn_edit)
        action_layout.addWidget(btn_del)
        action_widget.setLayout(action_layout)
        self.table.setCellWidget(row, 4, action_widget)
        # Centraliza o conteúdo da coluna Ação
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        # Mensagem de feedback se os ícones não forem encontrados
        if edit_icon.isNull() or del_icon.isNull():
            QMessageBox.warning(self, "Atenção", "Os botões de ação estão sem ícone. Verifique a pasta static/icons/solid/.")

    def get_table(self):
        return self.table
