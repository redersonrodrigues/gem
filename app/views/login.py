from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.database import get_engine

class LoginWindow(QWidget):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle('Login - Gestão de Escalas Médicas')
        self.setFixedSize(400, 400)  # Tamanho maior para acomodar o logo
        self.setup_ui()
        self.setWindowModality(Qt.ApplicationModal)
        self.input_user.setFocus()  # Foco inicial no campo usuário
        # Centralizar a tela de login
        self.center_on_screen()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        # Logo da empresa
        logo_label = QLabel()
        logo_pixmap = QPixmap('static/assets/images/logo.png')
        logo_label.setPixmap(logo_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        # Título
        title = QLabel('Bem-vindo ao GEM')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 18px; font-weight: bold; margin-bottom: 10px;')
        layout.addWidget(title)
        # Campos de login
        self.label_user = QLabel('Usuário:')
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText('Digite seu usuário')
        self.input_user.setFixedHeight(32)
        self.input_user.setStyleSheet('border-radius: 6px; padding: 6px; font-size: 14px;')
        self.label_pass = QLabel('Senha:')
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setPlaceholderText('Digite sua senha')
        self.input_pass.setFixedHeight(32)
        self.input_pass.setStyleSheet('border-radius: 6px; padding: 6px; font-size: 14px;')
        # Botão com ícone local FontAwesome
        self.btn_login = QPushButton('Entrar')
        icon_path = 'static/icons/solid/sign-in-alt.svg'
        import os
        if not os.path.exists(icon_path):
            icon_path = 'static/icons/solid/right-to-bracket.svg'  # fallback para FontAwesome 6
        if os.path.exists(icon_path):
            self.btn_login.setIcon(QIcon(icon_path))
        self.btn_login.setFixedHeight(36)
        self.btn_login.setStyleSheet('font-size: 15px; border-radius: 6px; padding: 6px; background-color: #1976d2; color: white;')
        self.btn_login.clicked.connect(self.try_login)
        # Botão fechar ao lado do Entrar
        self.btn_close = QPushButton('Fechar')
        self.btn_close.setStyleSheet('font-size: 15px; border-radius: 6px; padding: 6px; background-color: #d32f2f; color: white; font-weight: bold;')
        self.btn_close.setFixedHeight(36)
        self.btn_close.setFixedWidth(80)
        self.btn_close.clicked.connect(self.close)
        # Permitir login ao pressionar Enter
        self.input_user.returnPressed.connect(self.try_login)
        self.input_pass.returnPressed.connect(self.try_login)
        # Layout horizontal para botões centralizados
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_login)
        btn_layout.addSpacing(12)
        btn_layout.addWidget(self.btn_close)
        btn_layout.addStretch()
        # Adiciona campos ao layout
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        # Acessibilidade: Tab order
        self.setTabOrder(self.input_user, self.input_pass)
        self.setTabOrder(self.input_pass, self.btn_login)

    def try_login(self):
        print('Iniciando login')
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
        print(f'Usuário digitado: {username}')
        if not username or not password:
            print('Usuário ou senha em branco')
            QMessageBox.warning(self, 'Erro', 'Preencha usuário e senha.')
            return
        # Feedback visual: desabilita botão e cursor de espera
        self.btn_login.setEnabled(False)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        engine = get_engine()
        try:
            print('Abrindo sessão SQLAlchemy')
            with Session(engine) as session:
                print('Consultando usuário no banco')
                user = session.query(Usuario).filter_by(login=username).first()
                print(f'Usuário encontrado: {user}')
                if user:
                    print(f'Hash armazenado: {user.senha_hash}')
                if user and user.verificar_senha(password):
                    print('Senha verificada com sucesso')
                    if self.on_login_success:
                        try:
                            print('Chamando on_login_success')
                            self.on_login_success(user)
                            print('on_login_success chamado com sucesso')
                        except Exception as e:
                            print('Erro ao chamar on_login_success:', e)
                    self.close()
                else:
                    print('Usuário ou senha inválidos')
                    QMessageBox.critical(self, 'Erro', 'Usuário ou senha inválidos.')
        except Exception as e:
            import traceback
            print('Erro no login:', e)
            print(traceback.format_exc())
            QMessageBox.critical(self, 'Erro inesperado', f'Ocorreu um erro: {e}')
        finally:
            # Reabilita botão e cursor normal
            self.btn_login.setEnabled(True)
            QApplication.restoreOverrideCursor()
