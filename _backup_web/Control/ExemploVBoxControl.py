from Lib.Escala.Control.Page import Page
from Lib.Escala.Widgets.Container.Panel import Panel
from Lib.Escala.Widgets.Container.VBox import VBox


class ExemploVBoxControl(Page):
    def __init__(self):
        super().__init__()

        panel1 = Panel('Painel 1')
        panel1.style = 'margin:10px'
        panel1.add('painel 1')

        panel2 = Panel('Painel 2')
        panel2.style = 'margin:10px'
        panel2.add('painel 2')

        box = VBox()
        box.add(panel1)
        box.add(panel2)

        self.add(box)
