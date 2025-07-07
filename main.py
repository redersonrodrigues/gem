import sys
from PySide6.QtWidgets import QApplication
from Lib.Escala.Control.FrontController import FrontController


def main():
    app = QApplication(sys.argv)
    window = FrontController()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
