from Lib.Escala.Control.PageController import PageController
from Lib.Escala.Widgets.Dialog.Message import Message
from Lib.Escala.Widgets.Container.Panel import Panel
from Lib.Escala.Widgets.Button import Button
from Lib.Escala.Widgets.Container.VBox import VBox


class ExemploMessagePage(PageController):
    def __init__(self, app_controller):
        super().__init__(app_controller)
        panel = Panel("Exemplo de Mensagens")
        vbox = VBox()
        btn_info = Button("Mostrar mensagem informativa", "info")
        btn_info.clicked.connect(lambda: Message.show(
            'info', 'Mensagem informativa exibida com sucesso!'))
        btn_error = Button("Mostrar mensagem de erro", "danger")
        btn_error.clicked.connect(lambda: Message.show(
            'error', 'Ocorreu um erro ao executar a ação.'))
        vbox.add(btn_info)
        vbox.add(btn_error)
        vbox.add_stretch()
        panel.add(vbox)
        self.add(panel)

    def show(self, param=None):
        return self
