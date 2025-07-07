from Lib.Escala.Control.Page import Page
from Lib.Escala.Control.action import Action
from Lib.Escala.Widgets.Dialog.Question import Question
from Lib.Escala.Widgets.Dialog.Message import Message

class ExemploQuestionControl(Page):
    def __init__(self):
        super().__init__()
        action_yes = Action(self, 'onConfirma')
        action_yes.set_parameter('codigo', 1200)
        action_no = Action(self, 'onNega')
        self.add(Question('Você deseja confirmar?', action_yes, action_no))

    def onConfirma(self, param):
        self.add(Message('info', f"Confirmou a ação: {param}"))

    def onNega(self, param):
        self.add(Message('info', f"Negou a ação: {param}"))