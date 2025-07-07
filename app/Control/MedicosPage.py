from Lib.Escala.Control.PageController import PageController
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton

class MedicosPage(PageController):
    def __init__(self, app_controller):
        super().__init__(app_controller)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Cadastro de Médicos"))
        btn = QPushButton("Voltar ao Início")
        btn.clicked.connect(lambda: self.app_controller.show_page("HomePage"))
        layout.addWidget(btn)