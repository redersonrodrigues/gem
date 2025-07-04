import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

# === Framework loaders (Pablo Dall'Oglio style) ===
from Lib.Escala.Core.class_loader import ClassLoader
from Lib.Escala.Core.app_loader import AppLoader

# --- "Registra" os carregadores de classes (equivalente ao PHP spl_autoload_register) ---
# (Em Python, podemos apenas garantir que estão disponíveis para uso; os métodos estáticos simulam o autoload)


def load_template(path='app/Templates/template.html', context=None):
    context = context or {}
    with open(path, encoding='utf-8') as f:
        html = f.read()
    for key, value in context.items():
        html = html.replace('{' + key + '}', str(value))
    return html


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GEM - Gestão de Escala Médica")
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.show_page('Home')
        self.showMaximized()

    def show_page(self, class_name):
        try:
            # Carrega dinamicamente o Page Controller da aplicação (Pablo Dall'Oglio style)
            controller_cls = AppLoader.load_app_class(
                f"app.Control.{class_name}", class_name)
            controller = controller_cls()
            content = controller.show()  # O Page Controller retorna o HTML
        except Exception as e:
            content = f"<h2>Erro ao carregar página '{class_name}'</h2><pre>{e}</pre>"
        html = load_template(context={"content": content, "class": class_name})
        base_dir = os.path.abspath('app/Templates/')
        if not base_dir.endswith(os.sep):
            base_dir += os.sep
        self.browser.setHtml(html, baseUrl=QUrl.fromLocalFile(base_dir))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
