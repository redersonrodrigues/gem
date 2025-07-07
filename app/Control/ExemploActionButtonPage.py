from Lib.Escala.Control.PageController import PageController
from Lib.Escala.Control.Action import Action
from Lib.Escala.Widgets.Button import Button


class ExemploActionButtonPage(PageController):
    def __init__(self, app_controller):
        super().__init__(app_controller)
        button = Button('Ação', 'success')
        action = Action([self, 'executa_acao'])
        action.set_parameter('codigo', 4)
        action.set_parameter('nome', 'Teste')
        # Simula o href: ao clicar, imprime a query da ação
        button.clicked.connect(lambda: print(action.serialize()))
        self.add(button)

    def executa_acao(self, param=None):
        print(param)

    def show(self, param=None):
        return self
