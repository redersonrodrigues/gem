from .Field import Field
from ...Base.Element import Element

class Text(Field):
    """
    Representa uma caixa de texto (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, name):
        super().__init__(name)
        self.height = 100

    def setSize(self, width, height=None):
        self.size = width
        if height is not None:
            self.height = height

    def render(self):
        tag = Element('textarea')
        tag.class_ = 'field'
        tag.name = self.name
        tag.style = f"width:{self.size};height:{self.height}"
        if not self.getEditable():
            tag.readonly = '1'
        tag.add(str(self.value) if self.value is not None else '')
        for property, value in self.properties.items():
            setattr(tag, property, value)
        return tag.render()

    def __str__(self):
        return self.render()
