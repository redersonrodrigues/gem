from .Field import Field
from ...Base.Element import Element

class Entry(Field):
    """
    Classe para construção de caixas de texto (adaptado de Pablo Dall'Oglio)
    """
    def render(self):
        tag = Element('input')
        tag.class_ = 'field'
        tag.name = self.name
        tag.value = self.value
        tag.type = 'text'
        if self.size:
            tag.style = f"width:{self.size}"
        if not self.getEditable():
            tag.readonly = '1'
        for property, value in self.properties.items():
            setattr(tag, property, value)
        return tag.render()

    def __str__(self):
        return self.render()
