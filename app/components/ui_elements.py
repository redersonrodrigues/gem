"""
Componentes reutilizáveis de interface para PyQt5
"""
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTableWidget

class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)

class SearchField(QLineEdit):
    def __init__(self, placeholder='', parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("padding: 6px; border-radius: 4px; border: 1px solid #bbb;")

class StyledTable(QTableWidget):
    def __init__(self, rows, cols, parent=None):
        super().__init__(rows, cols, parent)
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background: #fafafa;
            }
            QHeaderView::section {
                background: #1976d2;
                color: white;
                font-weight: bold;
            }
        """)
        self.setAlternatingRowColors(True)
