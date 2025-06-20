# main.py - Ponto de entrada da aplicação GEM
# Estrutura básica para inicializar a interface PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GEM - Gestão de Escalas Médicas')
        self.setGeometry(100, 100, 800, 600)
        # Aqui você pode adicionar widgets e lógica inicial

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
