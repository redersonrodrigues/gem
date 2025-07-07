from Lib.Escala.Widgets.Container.Panel import Panel
from Lib.Escala.Widgets.Container.VBox import VBox
from PySide6.QtWidgets import QLabel, QPushButton
from Lib.Escala.Control.PageController import PageController


class TestVBoxPage(PageController):
    def __init__(self, app_controller):
        super().__init__(app_controller)
        panel = Panel("Teste VBox")
        vbox = VBox(spacing=18, margins=(10, 10, 10, 10))
        for i in range(1, 5):
            label = QLabel(f"Item vertical {i}")
            label.setStyleSheet(
                "background: #e3f2fd; padding: 12px; border-radius: 6px; font-size: 15px; color:black;")
            vbox.add(label)
        btn = QPushButton("Botão no VBox")
        btn.setStyleSheet(
            "background: #1976d2; color: #fff; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
        vbox.add(btn)
        vbox.add_stretch()
        panel.add(vbox)
        self.add(panel)

    def show(self, param=None):
        return self
