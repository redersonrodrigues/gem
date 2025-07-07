from Lib.Escala.Control.Page import Page
from Lib.Escala.Core.template_loader import TemplateLoader


class TemplateSampleControl(Page):
    def __init__(self):
        super().__init__()
        self.template_loader = TemplateLoader('app/Resources')

    def show(self, param=None):
        # Dados fixos (em produção, viriam do banco de dados)
        replaces = {
            'title': 'Título',
            'action': '?class=TemplateSampleControl&method=onGravar',
            'nome': 'Maria',
            'endereco': 'Rua das flores',
            'telefone': '(51) 1234-5678'
        }
        return self.template_loader.render('form.html', replaces)

    def onGravar(self, param):
        # Exibe os dados submetidos (simulação de POST)
        return f"<pre>{param}</pre>"
