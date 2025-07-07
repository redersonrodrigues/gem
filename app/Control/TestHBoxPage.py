from Lib.Escala.Widgets.Container.Panel import Panel
from Lib.Escala.Widgets.Container.HBox import HBox
from PySide6.QtWidgets import QLabel, QPushButton
from Lib.Escala.Control.PageController import PageController


class TestHBoxPage(PageController):
    def __init__(self, app_controller):
        super().__init__(app_controller)
        panel = Panel("Teste HBox")
        hbox = HBox(spacing=18, margins=(10, 10, 10, 10))
        for i in range(1, 5):
            label = QLabel(f"Item horizontal {i}")
            label.setStyleSheet(
                "background: #ffe082; padding: 12px; border-radius: 6px; font-size: 15px;")
            hbox.add(label)
        btn = QPushButton("Botão no HBox")
        btn.setStyleSheet(
            "background: #388e3c; color: #fff; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
        hbox.add(btn)
        hbox.add_stretch()
        panel.add(hbox)
        self.add(panel)

    def show(self, param=None):
        return self
