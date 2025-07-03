import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from Lib.Escala.Log.logger import get_logger
import os

logger = get_logger(__name__)

def load_template(path='app/Templates/template.html', context=None):
    """
    Carrega um template HTML e substitui marcadores simples.
    """
    context = context or {}
    try:
        with open(path, encoding='utf-8') as f:
            html = f.read()
        for key, value in context.items():
            html = html.replace('{' + key + '}', str(value))
        return html
    except Exception as e:
        logger.error(f"Falha ao carregar template: {e}")
        return "<h1>Erro ao carregar template</h1>"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GEM - Gestão de Escala Médica")
        self.setGeometry(100, 100, 900, 600)

        # Cria menu
        self._create_menu()

        # Cria o objeto browser para exibir o conteúdo web
        self.browser = QWebEngineView()

        # Carrega template inicial já com o conteúdo substituído
        html = load_template(context={"content": "<h2>Bem-vindo!</h2>"})
        self.browser.setHtml(html, baseUrl=QUrl.fromLocalFile(os.path.abspath('app/Templates/')))
        self.setCentralWidget(self.browser)

    def _create_menu(self):
        menu_bar = self.menuBar()

        # Define os itens do menu principal conforme solicitado
        menus = [
            ("Home", "home"),
            ("Médicos", "medicos"),
            ("Escalas", "escalas"),
            ("Especializações", "especializacoes"),
            ("Configurações", "configuracoes"),
            ("Relatórios", "relatorios"),
            ("Consultas", "consultas"),
            ("Dashboard", "dashboard"),
            ("Ajuda", "ajuda"),
            ("Contato", "contato")
        ]

        for label, key in menus:
            action = QAction(label, self)
            action.triggered.connect(lambda _, page=key: self.show_in_template(page))
            menu_bar.addAction(action)

    def show_in_template(self, page):
        """
        Troca o conteúdo do template HTML ao clicar nos menus, sem criar telas adicionais.
        """
        content_map = {
            "home": "<h2>Página principal da aplicação</h2>",
            "medicos": "<h2>Cadastro e Gestão de Médicos</h2>",
            "escalas": "<h2>Cadastro e Gestão de Escalas (Plantonistas/Sobreaviso)</h2>",
            "especializacoes": "<h2>Especializações</h2>",
            "configuracoes": "<h2>Configurações do Sistema (Admin)</h2>",
            "relatorios": "<h2>Relatórios</h2>",
            "consultas": "<h2>Consultas</h2>",
            "dashboard": "<h2>Dashboard</h2>",
            "ajuda": "<h2>Ajuda</h2>",
            "contato": "<h2>Contato</h2>",
        }
        html_content = content_map.get(page, "<h2>Página não encontrada</h2>")
        # Atualiza só o conteúdo dinâmico via JS
        js = f"setContent(`{html_content}`);"
        self.browser.page().runJavaScript(js)

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