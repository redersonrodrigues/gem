import sys
from PySide6.QtWidgets import QApplication
from app.views.login.login_view import LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    login.show()
    app.exec()
