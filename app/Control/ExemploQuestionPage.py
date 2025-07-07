from Lib.Escala.Control.PageController import PageController
from Lib.Escala.Widgets.Dialog.Question import Question


class ExemploQuestionPage(PageController):
    def __init__(self, app_controller):
        super().__init__(app_controller)
        from Lib.Escala.Widgets.Button import Button
        from Lib.Escala.Widgets.Container.VBox import VBox
        from Lib.Escala.Widgets.Container.Panel import Panel
        panel = Panel("Exemplo de Question")
        vbox = VBox()

        def on_confirma():
            Question('Você confirmou a ação!', lambda: None)

        def on_nega():
            Question('Você negou a ação!', lambda: None)
        btn_question = Button("Perguntar (Sim/Não)", "warning")
        btn_question.clicked.connect(lambda: Question(
            'Você deseja confirmar?', on_confirma, on_nega))
        vbox.add(btn_question)
        vbox.add_stretch()
        panel.add(vbox)
        self.add(panel)

    def show(self, param=None):
        return self
