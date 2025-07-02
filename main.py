import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from Lib.Escala.Core.class_loader import ClassLoader
from Lib.Escala.Core.app_loader import AppLoader
from Lib.Escala.Log.logger import get_logger

logger = get_logger(__name__)

def load_template(path='app/Templates/template.html'):
    """
    Lê um template HTML, se for necessário para relatórios ou interface híbrida.
    Não é usado diretamente na janela principal Qt, mas pode ser útil para futuras funções.
    """
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Falha ao carregar template: {e}")
        return "<h1>Erro ao carregar template</h1>"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GEM - Gestão de Escala Médica")
        self.setGeometry(100, 100, 900, 600)
        # Futuramente: adicionar widgets, menus, status bar, etc.

def main():
    logger.info("Iniciando aplicação GEM (Front Controller)...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        ret = app.exec()
        logger.info("Aplicação encerrada normalmente.")
        sys.exit(ret)
    except Exception as e:
        logger.error(f"Erro fatal na aplicação: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()