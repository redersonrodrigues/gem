import sys
from PySide6.QtWidgets import QApplication, QLabel


def main():
    app = QApplication(sys.argv)
    label = QLabel(
        "Teste PySide6 - Se você vê esta janela, PySide6 está funcionando!")
    label.resize(400, 100)
    label.show()
    app.exec()


if __name__ == "__main__":
    main()
