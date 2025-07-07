from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget,
    QMenu, QToolButton, QSizePolicy, QFrame
)
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import Qt, QSize
import os

def fa_icon(icon_name, size=20):
    icon_path = os.path.join(os.path.dirname(__file__), "assets/fontawesome", icon_name)
    return QIcon(icon_path)

class TemplateWindow(QWidget):
    """
    Template principal do app: cabeçalho, menu lateral (botões), rodapé e área de conteúdo dinâmico.
    """
    def __init__(self, app_controller):
        super().__init__()
        self.app_controller = app_controller

        self.setWindowState(Qt.WindowMaximized)  # Abrir maximizada

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ------------------- Cabeçalho -------------------
        header = QFrame()
        header.setStyleSheet("background: #2c3e50;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 4, 20, 4)
        header_layout.setSpacing(20)

        # Logo + Nome da aplicação (à esquerda)
        logo = QLabel()
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "../Images/logo_hepp.png"))
        pixmap = pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setFixedSize(54, 54)

        app_label = QLabel("GEM - Gestão de Escala Médica")
        app_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold; padding-left: 8px;")
        app_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        left_head = QHBoxLayout()
        left_head.addWidget(logo)
        left_head.addWidget(app_label)
        left_head.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        left_head.setSpacing(10)

        left_widget = QWidget()
        left_widget.setLayout(left_head)
        header_layout.addWidget(left_widget, stretch=1)

        # Menu suspenso à direita
        user_menu_btn = QToolButton()
        user_menu_btn.setIcon(fa_icon("user.png", 28))
        user_menu_btn.setIconSize(QSize(28, 28))
        user_menu_btn.setStyleSheet("color: white;")
        user_menu_btn.setPopupMode(QToolButton.InstantPopup)
        user_menu_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        user_menu_btn.setAutoRaise(True)

        user_menu = QMenu()
        action_login = QAction("Logar como administrador", self)
        action_login.setIcon(fa_icon("unlock.png", 18))
        action_login.triggered.connect(lambda: self.app_controller.show_page("LoginPage"))
        user_menu.addAction(action_login)

        action_exit = QAction("Sair", self)
        action_exit.setIcon(fa_icon("sign-out-alt.png", 18))
        action_exit.triggered.connect(self.app_controller.exit_application)
        user_menu.addAction(action_exit)

        user_menu_btn.setMenu(user_menu)
        header_layout.addWidget(user_menu_btn, stretch=0, alignment=Qt.AlignRight)
        header_layout.setAlignment(Qt.AlignVCenter)

        main_layout.addWidget(header)

        # ------------------- Centro: menu lateral + container -------------------
        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        main_layout.addLayout(center_layout, stretch=1)

        # Menu lateral (botões verticais com ícone)
        menu_frame = QFrame()
        menu_frame.setStyleSheet("background: #f2f2f2; border: none;")
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.setContentsMargins(0, 20, 0, 20)
        menu_layout.setSpacing(14)

        self.menu_buttons = []


        def add_menu_button(text, icon, page, tooltip="", parent_menu=None):
            btn = QPushButton(text)
            btn.setIcon(fa_icon(icon, 20))
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent; border: none;
                    padding: 10px 20px; text-align: left;
                    font-size: 12px; color: #333;
                }
                QPushButton:hover {
                    background: #e0e0e0;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda: self.app_controller.show_page(page))
            if tooltip:
                btn.setToolTip(tooltip)
            if parent_menu:
                parent_menu.addAction(btn.text(), lambda: self.app_controller.show_page(page))
            else:
                menu_layout.addWidget(btn)
                self.menu_buttons.append(btn)

        # Menus principais
        add_menu_button("Início", "home.png", "HomePage", "Tela inicial")
        add_menu_button("Médicos", "user-md.png", "MedicosPage", "Gestão de médicos")
        add_menu_button("Escalas", "calendar-alt.png", "EscalasPage", "Gestão de escalas")

        # Dropdown de Testes
        test_menu = QMenu("Testes", self)
        test_menu.setStyleSheet("QMenu { font-size: 13px; }")
        test_menu_btn = QToolButton()
        test_menu_btn.setText("Testes")
        test_menu_btn.setPopupMode(QToolButton.InstantPopup)
        test_menu_btn.setMenu(test_menu)
        test_menu_btn.setToolButtonStyle(Qt.ToolButtonTextOnly)
        test_menu_btn.setStyleSheet("""
            QToolButton {
                padding: 10px 20px;
                text-align: left;
                font-size: 12px;
                color: #333;
                background: transparent;
                border: none;
                qproperty-icon: none;
            }
            QToolButton::menu-indicator {
                subcontrol-position: right center;
                left: 4px;
            }
        """)
        test_menu_btn.setCursor(Qt.PointingHandCursor)
        test_menu_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        test_menu_btn.setLayoutDirection(Qt.LeftToRight)
        menu_layout.addWidget(test_menu_btn, alignment=Qt.AlignLeft)

        # Submenus de teste
        test_menu.addAction("Teste VBox", lambda: self.app_controller.show_page("TestVBoxPage"))
        test_menu.addAction("Teste HBox", lambda: self.app_controller.show_page("TestHBoxPage"))
        test_menu.addSeparator()
        test_menu.addAction("Exemplo Message", lambda: self.app_controller.show_page("ExemploMessagePage"))
        test_menu.addAction("Exemplo Question", lambda: self.app_controller.show_page("ExemploQuestionPage"))
        test_menu.addSeparator()
        test_menu.addAction("Exemplo Action", lambda: self.app_controller.show_page("ExemploActionPage"))
        test_menu.addAction("Exemplo Action Button", lambda: self.app_controller.show_page("ExemploActionButtonPage"))

        menu_layout.addStretch(1)
        menu_frame.setFixedWidth(180)
        center_layout.addWidget(menu_frame)

        # Container do conteúdo dinâmico
        self.container = QStackedWidget()
        self.container.setStyleSheet("background: #fff; border: none;")
        center_layout.addWidget(self.container, stretch=1)

        # ------------------- Rodapé -------------------
        footer = QLabel("Rodapé - GEM © 2025")
        footer.setStyleSheet("background: #2c3e50; color: #aaa; padding: 8px; font-size: 12px;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        # ---- Inicialização: a HomePage será carregada pelo controller principal ----
        # (Removido o show_page daqui para evitar dependência cíclica)

    def set_content(self, widget: QWidget):
        """Troca o conteúdo central."""
        print(f"[DEBUG] set_content: exibindo widget {widget}")
        idx = self.container.indexOf(widget)
        if idx == -1:
            self.container.addWidget(widget)
            idx = self.container.indexOf(widget)
        self.container.setCurrentIndex(idx)
        self.container.update()
        widget.update()
        widget.repaint()