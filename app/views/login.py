from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.database import get_engine

class LoginWindow(QWidget):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle('Login - Gestão de Escalas Médicas')
        self.setFixedSize(350, 200)
        self.setup_ui()
        self.setWindowModality(Qt.ApplicationModal)

    def setup_ui(self):
        layout = QVBoxLayout()
        self.label_user = QLabel('Usuário:')
        self.input_user = QLineEdit()
        self.label_pass = QLabel('Senha:')
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.btn_login = QPushButton('Entrar')
        self.btn_login.clicked.connect(self.try_login)
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)

    def try_login(self):
        print('Iniciando login')
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
        print(f'Usuário digitado: {username}')
        if not username or not password:
            print('Usuário ou senha em branco')
            QMessageBox.warning(self, 'Erro', 'Preencha usuário e senha.')
            return
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
