"""
Main application window (PyQt5) - View principal
"""

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt
from .medicos_view import MedicosView
from .especializacoes_view import EspecializacoesView
from .escalas_view import EscalasView
from .logs_view import LogsView
from .ajuda_view import AjudaView
from .login import LoginWindow
from app.components.themes import LIGHT_THEME, DARK_THEME
from app.core.backend_bridge import BackendBridge
from app.utils.integrity_checker import IntegrityChecker


class MainWindow(QMainWindow):
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario  # Usuário logado
        self.perfil = usuario.perfil if usuario else None
        self.setWindowTitle("GEM - Gestão de Escalas Médicas")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self._views = {}  # Mapeamento de views por nome
        self._tema_escuro = False  # Estado do tema
        # Instanciar backend e checker
        self.backend_bridge = BackendBridge("http://localhost:5000")
        self.integrity_checker = IntegrityChecker(self.backend_bridge)
        self.init_ui()
        self.showMaximized()  # Abre a janela principal já maximizada

    def logout(self):
        self.close()
        self.login_window = LoginWindow(on_login_success=self._on_login_success)
        self.login_window.show()

    def _on_login_success(self, usuario):
        self.__init__(usuario)
        self.show()

    def init_ui(self):
        # Menu lateral para navegação
        from PyQt5.QtWidgets import QDockWidget, QListWidget
        dock = QDockWidget("Menu", self)
        menu = QListWidget()
        menu.addItem("Médicos")
        menu.addItem("Especializações")
        menu.addItem("Escalas")
        menu.addItem("Logs")
        menu.addItem("Ajuda")
        dock.setWidget(menu)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        # Instanciar views com checker e perfil
        self.medicos_view = MedicosView(integrity_checker=self.integrity_checker, perfil=self.perfil)
        self.especializacoes_view = EspecializacoesView(integrity_checker=self.integrity_checker, perfil=self.perfil)
        self.escalas_view = EscalasView(integrity_checker=self.integrity_checker, perfil=self.perfil)
        self.logs_view = LogsView()
        self.ajuda_view = AjudaView()
        self.add_view(self.medicos_view, "Médicos")
        self.add_view(self.especializacoes_view, "Especializações")
        self.add_view(self.escalas_view, "Escalas")
        self.add_view(self.logs_view, "Logs")
        self.add_view(self.ajuda_view, "Ajuda")

        # Troca de tela ao clicar no menu
        menu.currentRowChanged.connect(self._on_menu_change)
        self.menu = menu
        self.central_widget.setCurrentWidget(self.medicos_view)

        # Botão de troca de tema
        from PyQt5.QtWidgets import QToolBar, QAction
        toolbar = QToolBar("Temas", self)
        self.addToolBar(toolbar)
        self._action_tema = QAction("Modo Escuro", self)
        self._action_tema.setCheckable(True)
        self._action_tema.toggled.connect(self.toggle_tema)
        toolbar.addAction(self._action_tema)
        self.apply_theme()

    def add_view(self, widget: QWidget, name: str):
        self.central_widget.addWidget(widget)
        # Para navegação futura: self.central_widget.setCurrentWidget(widget)
        # Mapeamento de views por nome para navegação
        self._views[name] = widget

    def show_view(self, name: str):
        if hasattr(self, '_views') and name in self._views:
            self.central_widget.setCurrentWidget(self._views[name])

    def _on_menu_change(self, index):
        if index == 0:
            self.central_widget.setCurrentWidget(self.medicos_view)
        elif index == 1:
            self.central_widget.setCurrentWidget(self.especializacoes_view)
        elif index == 2:
            self.central_widget.setCurrentWidget(self.escalas_view)
        elif index == 3:
            self.central_widget.setCurrentWidget(self.logs_view)
        elif index == 4:
            self.central_widget.setCurrentWidget(self.ajuda_view)

    def toggle_tema(self, checked):
        self._tema_escuro = checked
        self.apply_theme()
        self._action_tema.setText("Modo Claro" if checked else "Modo Escuro")

    def apply_theme(self):
        if getattr(self, '_tema_escuro', False):
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)

    def resizeEvent(self, event):
        # Garante que o central_widget ocupe todo o espaço disponível
        self.central_widget.setGeometry(self.rect())
        super().resizeEvent(event)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    def start_main(usuario):
        window = MainWindow(usuario)
        window.show()
    login = LoginWindow(on_login_success=start_main)
    login.show()
    sys.exit(app.exec_())
