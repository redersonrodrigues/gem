from Lib.Escala.Widgets.Base.Element import Element


class VBox(Element):
    """
    Caixa vertical (VBox) - empacota elementos verticalmente em blocos.
    Inspirado em Pablo Dall'Oglio.
    """

    def __init__(self):
        super().__init__('div')
        # Em Bootstrap 5, 'd-flex flex-column' é a abordagem mais adequada para VBox
        # gap-2 adiciona espaçamento entre itens
        self.class_ = 'd-flex flex-column gap-2'

