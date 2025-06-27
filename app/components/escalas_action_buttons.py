from PyQt5.QtWidgets import QWidget, QHBoxLayout
from app.components.ui_elements import PrimaryButton
from app.components.icon_helper import get_icon

class EscalasActionButtons(QWidget):
    def __init__(self, on_add=None, on_export=None, on_import=None, on_print=None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.add_btn = PrimaryButton("Adicionar Escala")
        self.add_btn.setIcon(get_icon("add"))
        if on_add:
            self.add_btn.clicked.connect(on_add)
        layout.addWidget(self.add_btn)

        self.export_btn = PrimaryButton("Exportar CSV")
        self.export_btn.setIcon(get_icon("download"))
        if on_export:
            self.export_btn.clicked.connect(on_export)
        layout.addWidget(self.export_btn)

        self.import_btn = PrimaryButton("Importar CSV")
        self.import_btn.setIcon(get_icon("upload"))
        if on_import:
            self.import_btn.clicked.connect(on_import)
        layout.addWidget(self.import_btn)

        self.print_btn = PrimaryButton("Imprimir Relatório")
        self.print_btn.setIcon(get_icon("calendar"))
        if on_print:
            self.print_btn.clicked.connect(on_print)
        layout.addWidget(self.print_btn)

        self.filtrar_btn = PrimaryButton("Filtrar")
        self.filtrar_btn.setIcon(get_icon("search"))
        layout.addWidget(self.filtrar_btn)

        self.limpar_btn = PrimaryButton("Limpar Filtros")
        self.limpar_btn.setIcon(get_icon("eraser"))
        layout.addWidget(self.limpar_btn)

        self.setLayout(layout)
