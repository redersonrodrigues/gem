from Lib.Escala.Control.Page import Page
from Lib.Escala.Widgets.Container.Panel import Panel


class ExemploPanelControl(Page):
    def __init__(self):
        super().__init__()

        # Cria o painel com título
        panel = Panel('Título Painel Elegante')
        # Bootstrap classes para elegância
        panel.class_ = 'panel panel-default shadow rounded border border-dark'
        # Centraliza e limita largura para visual moderno
        panel.style = 'margin: 32px auto; max-width: 480px;'

        # Header elegante
        if panel.children:
            header = panel.children[0]
            header.class_ = 'panel-heading bg-primary text-white border-bottom border-dark rounded-top'
            header.style = 'padding: 18px; font-size: 1.4rem; letter-spacing: 1px;'

            # Se o título for um h4 dentro do header:
            if hasattr(header, 'children') and header.children:
                header_title = header.children[0]  # .panel-title
                header_title.class_ = 'panel-title'
                if hasattr(header_title, 'children') and header_title.children:
                    h4 = header_title.children[0]
                    h4.class_ = 'm-0'

        # Corpo com visual mais limpo
        panel.body.class_ = 'panel-body bg-light border-bottom border-dark'
        panel.body.style = 'padding: 28px; font-size: 1.1rem; color: #2d2d2d;'

        # Conteúdo do painel
        panel.add(
            'Exemplo de painel elegante usando classes do <b>Bootstrap</b>. Personalize facilmente o visual!')

        # Rodapé elegante
        panel.footer.class_ = 'panel-footer bg-secondary text-white border-dark rounded-bottom'
        panel.footer.style = 'padding: 14px; font-size: 1rem; text-align: right;'
        panel.add_footer('rodapé elegante')

        # Adiciona o painel à página
        self.add(panel)
