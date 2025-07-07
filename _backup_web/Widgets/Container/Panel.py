from Lib.Escala.Widgets.Base.Element import Element


class Panel(Element):
    """
    Empacota elementos em painel Bootstrap 5 (card)
    Inspirado em Pablo Dall'Oglio.
    """

    def __init__(self, panel_title=None):
        super().__init__('div')
        # Bootstrap 5 utiliza 'card'
        self.class_ = 'card shadow-sm mb-3'

        # Título do painel (opcional)
        if panel_title:
            head = Element('div')
            head.class_ = 'card-header'
            label = Element('h4')
            label.class_ = 'card-title mb-0'
            label.add(panel_title)
            head.add(label)
            super().add(head)

        # Corpo do painel
        self.body = Element('div')
        self.body.class_ = 'card-body'
        super().add(self.body)

        # Rodapé do painel (opcional, só adicionado se usar add_footer)
        self.footer = Element('div')
        self.footer.class_ = 'card-footer d-none'  # Oculto por padrão

    def add(self, child):
        """
        Adiciona conteúdo ao corpo do painel
        """
        self.body.add(child)

    def add_footer(self, footer):
        """
        Adiciona conteúdo ao rodapé do painel
        """
        self.footer.add(footer)
        self.footer.class_ = 'card-footer'  # Remove ocultação
        super().add(self.footer)
