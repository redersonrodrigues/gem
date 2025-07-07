from Lib.Escala.Control.PageController import PageController
from Lib.Escala.Control.Action import Action


class ExemploActionPage(PageController):
    def __init__(self, app_controller):
        super().__init__(app_controller)
        # Cria a ação e define parâmetros
        action = Action([self, 'executa_acao'])
        action.set_parameter('codigo', 4)
        action.set_parameter('nome', 'teste')
        # Exibe a string serializada (query)
        print(action.serialize())

    def executa_acao(self):
        pass

    def show(self, param=None):
        return self
