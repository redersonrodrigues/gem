from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QMessageBox, QApplication
from PySide6.QtUiTools import QUiLoader
from app.controllers.login.login_controller import LoginController


class LoginDialog:
    def __init__(self):
        loader = QUiLoader()
        ui_path = r"C:\Users\rrodrigues\Desktop\gem\app\templates\login\tela_login.ui"
        self.ui = loader.load(ui_path, None)

        self.txtUser = self.ui.findChild(QLineEdit, "txtUser")
        self.txtPassword = self.ui.findChild(QLineEdit, "txtPassword")
        self.btnEntrar = self.ui.findChild(QPushButton, "btnEntrar")
        self.btnFechar = self.ui.findChild(QPushButton, "btnFechar")

        self.controller = LoginController(self)
        self.btnEntrar.clicked.connect(self.on_login)
        self.btnFechar.clicked.connect(self.on_fechar)
        self.txtPassword.returnPressed.connect(self.on_login)
        self.txtUser.returnPressed.connect(self.txtPassword.setFocus)

        self.user = None  # guarda o usuário logado

    def show(self):
        return self.ui.exec_()

    def on_login(self):
        email = self.txtUser.text().strip()
        senha = self.txtPassword.text().strip()
        user = self.controller.login(email, senha)
        if user:
            self.user = user
            self.ui.accept()

    def on_fechar(self):
        self.ui.reject()
        QApplication.quit()

    def show_error(self, msg):
        QMessageBox.critical(self.ui, "Erro de Login", msg)
