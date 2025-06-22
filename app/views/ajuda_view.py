"""
Tela de Ajuda e Suporte (FAQs e contato)
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import Qt

class AjudaView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ajuda_view")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        title = QLabel("Ajuda e Suporte")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(title)

        faq = QTextEdit()
        faq.setReadOnly(True)
        faq.setHtml("""
        <h3>Perguntas Frequentes (FAQ)</h3>
        <ul>
        <li><b>Como cadastrar um médico?</b> Use a tela de Médicos e clique em 'Adicionar Médico'.</li>
        <li><b>Como buscar uma escala?</b> Use o campo de busca na tela de Escalas.</li>
        <li><b>Como alterar minha senha?</b> Acesse o menu de usuário e selecione 'Alterar Senha'.</li>
        <li><b>Como exportar relatórios?</b> Use a opção de impressão/exportação na tela de relatórios.</li>
        </ul>
        <h3>Suporte Técnico</h3>
        <p>Em caso de dúvidas ou problemas, envie um e-mail para <a href='mailto:suporte@gemapp.com'>suporte@gemapp.com</a>.</p>
        """)
        self.layout.addWidget(faq)

        contato_btn = QPushButton("Entrar em contato com o suporte")
        contato_btn.clicked.connect(self.contato_suporte)
        self.layout.addWidget(contato_btn)

    def contato_suporte(self):
        from app.components.notifier import Notifier
        Notifier.info(self, "Suporte", "E-mail enviado para o suporte!")
