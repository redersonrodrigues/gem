# main.py - Ponto de entrada da aplicação GEM
# Estrutura básica para inicializar a interface PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QPushButton
from app.core.database import init_db
from app.models import audit_listener
from app.views.login import LoginWindow


class MainWindow(QMainWindow):
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle('GEM - Gestão de Escalas Médicas')
        self.setGeometry(100, 100, 800, 600)
        # Exemplo: exibir nome e perfil do usuário logado
        if self.usuario:
            self.statusBar().showMessage(
                f'Usuário: {self.usuario.nome} | Perfil: {self.usuario.perfil}'
            )
        # Menu principal
        menubar = self.menuBar()
        menubar.addMenu('Arquivo')
        # Menu administrativo (restrito)
        if (
            self.usuario and hasattr(self.usuario, 'is_admin')
            and self.usuario.is_admin()
        ):
            menu_admin = menubar.addMenu('Administração')
            acao_usuarios = QAction('Gerenciar Usuários', self)
            menu_admin.addAction(acao_usuarios)
            # Exemplo: botão restrito a admin
            self.btn_admin = QPushButton('Ação Restrita (Admin)', self)
            self.btn_admin.setGeometry(50, 80, 200, 40)
            self.btn_admin.show()
        else:
            # Usuário comum não vê o menu/botão admin
            self.btn_admin = None
            self.setWindowTitle(self.windowTitle() + ' [USUÁRIO]')


if __name__ == '__main__':
    # Inicializa o banco e registra listeners de auditoria
    init_db()
    print("Banco de dados inicializado com sucesso!")
    app = QApplication(sys.argv)

    usuario_autenticado = {'user': None}

    def on_login_success(user):
        usuario_autenticado['user'] = user

    login_window = LoginWindow(on_login_success=on_login_success)
    login_window.show()
    app.exec_()

    if usuario_autenticado['user']:
        window = MainWindow(usuario=usuario_autenticado['user'])
        window.show()
        sys.exit(app.exec_())
