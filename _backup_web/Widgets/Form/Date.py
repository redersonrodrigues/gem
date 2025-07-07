from .Entry import Entry
from ...Base.Element import Element

class Date(Entry):
    """
    Classe para construção de caixas de texto do tipo data (adaptado de Pablo Dall'Oglio)
    """
    def render(self):
        tag = Element('input')
        tag.class_ = 'field'
        tag.name = self.name
        tag.value = self.value
        tag.type = 'date'
        if self.size:
            tag.style = f"width:{self.size}"
        if not self.getEditable():
            tag.readonly = '1'
        for property, value in self.properties.items():
            setattr(tag, property, value)
        return tag.render()

    def __str__(self):
        return self.render()
