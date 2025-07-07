from Lib.Escala.Widgets.Base.Element import Element


class HBox(Element):
    """
    Caixa horizontal (HBox) - empacota elementos lado a lado em blocos inline.
    Inspirado em Pablo Dall'Oglio.
    """

    def __init__(self):
        super().__init__('div')
        # Bootstrap 5: flex row e alinhamento ao topo por padrão
        self.class_ = 'd-flex flex-row gap-2 align-items-start'

