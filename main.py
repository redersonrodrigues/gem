# main.py - Ponto de entrada da aplicação GEM
# Estrutura básica para inicializar a interface PyQt5

import sys
from PyQt5.QtWidgets import QApplication
from app.views.login import LoginWindow
from app.views.main_window import MainWindow
from app import create_app

if __name__ == '__main__':
    flask_app = create_app()
    app = QApplication(sys.argv)
    main_window = None
    ctx = None
    def start_main(usuario):
        global main_window, ctx
        # Mantém o contexto ativo durante toda a execução da interface
        if ctx is None:
            ctx = flask_app.app_context()
            ctx.push()
        main_window = MainWindow(usuario)
        main_window.show()
    login = LoginWindow(on_login_success=start_main)
    login.show()
    sys.exit(app.exec_())
