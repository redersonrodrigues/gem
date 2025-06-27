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
from PyQt5.QtWidgets import QDockWidget, QTreeWidget, QTreeWidgetItem, QToolBar, QAction, QMessageBox, QFrame, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
import os
from app.views.escalas.plantonistas.plantonistas_view import PlantonistasView
from app.views.escalas.sobreavisos.sobreavisos_view import SobreavisosView


class MainWindow(QMainWindow):
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario  # Usuário logado
        self.perfil = usuario.perfil if usuario else None
        self.setWindowTitle("GEM - Gestão de Escalas Médicas")
        # Remove restrições de tamanho fixo
        self.setMinimumSize(800, 600)
        self.setMaximumSize(16777215, 16777215)
        self.setGeometry(QApplication.primaryScreen().availableGeometry())
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
        self.showMaximized()

    def init_ui(self):
        dock = QDockWidget("Menu", self)
        menu = QTreeWidget()
        menu.setHeaderHidden(True)
        # Ícones exclusivos para cada item
        from PyQt5.QtGui import QIcon, QPixmap
        icon_medicos = QIcon('static/icons/solid/user.svg')
        icon_especializacoes = QIcon('static/icons/solid/stethoscope.svg')
        icon_escalas = QIcon('static/icons/solid/calendar-alt.svg') if os.path.exists('static/icons/solid/calendar-alt.svg') else QIcon('static/icons/solid/calendar.svg')
        icon_plantonista = QIcon('static/icons/solid/user-nurse.svg') if os.path.exists('static/icons/solid/user-nurse.svg') else QIcon('static/icons/solid/user.svg')
        icon_sobreaviso = QIcon('static/icons/solid/bell.svg')
        icon_logs = QIcon('static/icons/solid/file.svg')
        # Tenta solid/question-circle.svg, senão regular/question-circle.svg
        ajuda_pixmap = QPixmap('static/icons/solid/question.svg')
        if not ajuda_pixmap.isNull():
            # Colore o pixmap de azul
            ajuda_pixmap_colored = QPixmap(ajuda_pixmap.size())
            ajuda_pixmap_colored.fill(Qt.transparent)
            from PyQt5.QtGui import QPainter, QColor
            painter = QPainter(ajuda_pixmap_colored)
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            painter.drawPixmap(0, 0, ajuda_pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(ajuda_pixmap_colored.rect(), QColor('#1976d2'))
            painter.end()
            icon_ajuda = QIcon(ajuda_pixmap_colored)
        else:
            icon_ajuda = QIcon('static/icons/solid/question.svg')
        # Sair vermelho
        sair_pixmap = QPixmap('static/icons/solid/right-from-bracket.svg')
        if not sair_pixmap.isNull():
            sair_pixmap_colored = QPixmap(sair_pixmap.size())
            sair_pixmap_colored.fill(Qt.transparent)
            painter = QPainter(sair_pixmap_colored)
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            painter.drawPixmap(0, 0, sair_pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(sair_pixmap_colored.rect(), QColor('#d32f2f'))
            painter.end()
            icon_sair = QIcon(sair_pixmap_colored)
        else:
            icon_sair = QIcon('static/icons/solid/right-from-bracket.svg')
        # Itens principais
        item_medicos = QTreeWidgetItem(["Médicos"])
        item_medicos.setIcon(0, icon_medicos)
        item_especializacoes = QTreeWidgetItem(["Especializações"])
        item_especializacoes.setIcon(0, icon_especializacoes)
        # Escalas com subitens
        item_escalas = QTreeWidgetItem(["Escalas"])
        item_escalas.setIcon(0, icon_escalas)
        subitem_plantonista = QTreeWidgetItem(["Plantonista"])
        subitem_plantonista.setIcon(0, icon_plantonista)
        subitem_sobreaviso = QTreeWidgetItem(["Sobreaviso"])
        subitem_sobreaviso.setIcon(0, icon_sobreaviso)
        item_escalas.addChildren([subitem_plantonista, subitem_sobreaviso])
        item_escalas.setExpanded(False)  # Começa retraído
        # Separador visual
        item_sep1 = QTreeWidgetItem(["-------------------"])
        item_sep1.setFlags(item_sep1.flags() & ~Qt.ItemIsSelectable)
        # Logs e Ajuda
        item_logs = QTreeWidgetItem(["Logs"])
        item_logs.setIcon(0, icon_logs)
        item_ajuda = QTreeWidgetItem(["Ajuda"])
        item_ajuda.setIcon(0, icon_ajuda)
        # Separador visual
        item_sep2 = QTreeWidgetItem(["-------------------"])
        item_sep2.setFlags(item_sep2.flags() & ~Qt.ItemIsSelectable)
        # Sair
        item_sair = QTreeWidgetItem(["Sair"])
        item_sair.setIcon(0, icon_sair)
        # Monta menu
        menu.addTopLevelItems([
            item_medicos,
            item_especializacoes,
            item_escalas,
            item_sep1,
            item_logs,
            item_ajuda,
            item_sep2,
            item_sair
        ])
        menu.setMaximumWidth(220)
        dock.setWidget(menu)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        # Tela principal de dashboard
        self.dashboard_view = QWidget()
        dash_layout = QVBoxLayout()
        dash_layout.setAlignment(Qt.AlignCenter)
        dash_img = QLabel()
        dash_pixmap = QPixmap('static/assets/images/img_dashboard.png')
        dash_img.setPixmap(dash_pixmap.scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        dash_img.setAlignment(Qt.AlignCenter)
        dash_layout.addWidget(dash_img)
        msg = QLabel(f"Bem-vindo(a), {self.usuario.nome if self.usuario else ''}!\nSelecione uma opção no menu à esquerda para começar.")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet('font-size: 20px; font-weight: bold; margin-top: 20px;')
        dash_layout.addWidget(msg)
        self.dashboard_view.setLayout(dash_layout)
        self.add_view(self.dashboard_view, "Dashboard")

        # Instanciar views com checker e perfil
        self.medicos_view = MedicosView(integrity_checker=self.integrity_checker, perfil=self.perfil)
        self.especializacoes_view = EspecializacoesView(integrity_checker=self.integrity_checker, perfil=self.perfil)
        self.escalas_plantonista_view = PlantonistasView(integrity_checker=self.integrity_checker, perfil=self.perfil)
        self.escalas_sobreaviso_view = SobreavisosView(integrity_checker=self.integrity_checker, perfil=self.perfil)
        self.logs_view = LogsView()
        self.ajuda_view = AjudaView()
        self.add_view(self.medicos_view, "Médicos")
        self.add_view(self.especializacoes_view, "Especializações")
        self.add_view(self.escalas_plantonista_view, "Plantonista")
        self.add_view(self.escalas_sobreaviso_view, "Sobreaviso")
        self.add_view(self.logs_view, "Logs")
        self.add_view(self.ajuda_view, "Ajuda")

        # Troca de tela ao clicar no menu
        menu.itemClicked.connect(self._on_menu_change)
        self.menu = menu
        self.central_widget.setCurrentWidget(self.dashboard_view)

        # Botão de troca de tema
        toolbar = QToolBar("Temas", self)
        self.addToolBar(toolbar)
        self._action_tema = QAction("Modo Escuro", self)
        self._action_tema.setCheckable(True)
        self._action_tema.toggled.connect(self.toggle_tema)
        toolbar.addAction(self._action_tema)
        # Botão de ação restrita (apenas admin)
        if self.perfil == 'admin':
            self._action_restrita = QAction("Ação Restrita (Admin)", self)
            self._action_restrita.triggered.connect(self.acao_restrita_admin)
            toolbar.addAction(self._action_restrita)
        self.apply_theme()

        # Fundo branco para a tela principal
        self.central_widget.setStyleSheet('background-color: white;')

    def add_view(self, widget: QWidget, name: str):
        self.central_widget.addWidget(widget)
        # Para navegação futura: self.central_widget.setCurrentWidget(widget)
        # Mapeamento de views por nome para navegação
        self._views[name] = widget

    def show_view(self, name: str):
        if hasattr(self, '_views') and name in self._views:
            self.central_widget.setCurrentWidget(self._views[name])

    def _on_menu_change(self, item, column=0):
        text = item.text(0)
        if text == "Médicos":
            self.central_widget.setCurrentWidget(self.medicos_view)
        elif text == "Especializações":
            self.central_widget.setCurrentWidget(self.especializacoes_view)
        elif text == "Plantonista":
            self.central_widget.setCurrentWidget(self.escalas_plantonista_view)
        elif text == "Sobreaviso":
            self.central_widget.setCurrentWidget(self.escalas_sobreaviso_view)
        elif text == "Logs":
            self.central_widget.setCurrentWidget(self.logs_view)
        elif text == "Ajuda":
            self.central_widget.setCurrentWidget(self.ajuda_view)
        elif text == "Sair":
            from PyQt5.QtWidgets import QMessageBox, QPushButton
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Confirmação")
            msg_box.setText("Deseja realmente sair da aplicação?")
            btn_sim = msg_box.addButton("Sim", QMessageBox.YesRole)
            btn_nao = msg_box.addButton("Não", QMessageBox.NoRole)
            msg_box.setDefaultButton(btn_nao)
            msg_box.exec_()
            if msg_box.clickedButton() == btn_sim:
                self.logout()
        # Ao clicar em "Escalas" não faz nada (mantém dashboard ou tela atual)

    def toggle_tema(self, checked):
        self._tema_escuro = checked
        self.apply_theme()
        self._action_tema.setText("Modo Claro" if checked else "Modo Escuro")

    def apply_theme(self):
        if getattr(self, '_tema_escuro', False):
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)

    def acao_restrita_admin(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Ação Restrita", "Ação exclusiva para administradores executada com sucesso!")
        print("Ação restrita de admin executada.")

    def resizeEvent(self, event):
        # Garante que o central_widget ocupe todo o espaço disponível
        self.central_widget.setGeometry(self.rect())
        super().resizeEvent(event)
        # Força ocupar toda a tela disponível
        self.setGeometry(QApplication.primaryScreen().availableGeometry())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    def start_main(usuario):
        window = MainWindow(usuario)
        window.showMaximized()
    login = LoginWindow(on_login_success=start_main)
    login.show()
    sys.exit(app.exec_())
