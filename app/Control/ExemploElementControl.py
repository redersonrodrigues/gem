from Lib.Escala.Control.Page import Page
from Lib.Escala.Widgets.Base.element import Element

class ExemploElementControl(Page):
    def __init__(self):
        super().__init__()

        div = Element('div')
        # Adicionando múltiplos estilos (como no exemplo em PHP)
        div.style = 'text-align:center; font-weight:bold; font-size:14pt; margin:20px;'

        p = Element('p')
        p.add('Isto é um teste de parágrafo')

        div.add(p)

        # Adicione mais elementos se quiser, exemplo:
        # img = Element('img')
        # img.src = 'inter.png'
        # div.add(img)
        #
        # outro_p = Element('p')
        # outro_p.add('Clube do povo do Rio Grande do Sul')
        # div.add(outro_p)

        # Adiciona a div na página (Page também precisa implementar add/show)
        self.add(div)