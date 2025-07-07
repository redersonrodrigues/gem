
from Lib.Escala.Control.Page import Page
from Lib.Escala.Widgets.Dialog.Message import Message


class ExemploMessageControl(Page):
    def __init__(self):
        super().__init__()
        self.add(Message('info',  'Mensagem informativa'))
        self.add(Message('error', 'Mensagem de erro'))
