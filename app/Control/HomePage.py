from Lib.Escala.Control.PageController import PageController
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from Lib.Escala.Widgets.Container.Panel import Panel


class HomePage(PageController):
    def __init__(self, app_controller):
        super().__init__(app_controller)
        # Cor de fundo suave
        self.setStyleSheet("background: #f5f5f5;")

        # Painel central estilizado
        panel = Panel()
        panel.setStyleSheet(
            "QGroupBox { background: #fff; border: 2px solid #1976d2; border-radius: 12px; margin-top: 12px; }"
        )

        # Layout vertical centralizado
        from Lib.Escala.Widgets.Base.Image import Image
        from PySide6.QtGui import QFont
        from PySide6.QtCore import Qt

        # Título
        titulo = QLabel("Sistema de Controle de Escalas Médicas")
        titulo.setFont(QFont("Arial", 22, QFont.Bold))
        titulo.setStyleSheet("color: #1976d2; margin-bottom: 12px;")
        titulo.setAlignment(Qt.AlignCenter)
        panel.add(titulo)

        # Subtítulo
        subtitulo = QLabel("Hospital Estadual Porto Primavera")
        subtitulo.setFont(QFont("Arial", 16))
        subtitulo.setStyleSheet("color: #555; margin-bottom: 18px;")
        subtitulo.setAlignment(Qt.AlignCenter)
        panel.add(subtitulo)

        # Imagem centralizada usando componente Image
        img = Image("app/images/home.png", width=320, height=220)
        panel.add(img)

        panel.add_stretch()
        self.add(panel)

    def show(self, param=None):
        # Retorna o próprio widget (self) para exibição
        return self
