"""
Tela de consulta de logs do sistema
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import datetime
import os
from app.components.ui_logger import LOG_PATH

class LogsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("logs_view")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        title = QLabel("Histórico de Logs do Sistema")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(title)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Data/Hora", "Usuário", "Ação", "Detalhes"])
        self.layout.addWidget(self.table)
        self.carregar_logs()

    def carregar_logs(self):
        self.table.setRowCount(0)
        if not os.path.exists(LOG_PATH):
            return
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(line.strip()))
