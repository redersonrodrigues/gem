from .Field import Field
from ...Base.Element import Element

class Hidden(Field):
    """
    Representa um campo escondido (adaptado de Pablo Dall'Oglio)
    """
    def render(self):
        tag = Element('input')
        tag.class_ = 'field'
        tag.name = self.name
        tag.value = self.value
        tag.type = 'hidden'
        if self.size:
            tag.style = f"width:{self.size}"
        for property, value in self.properties.items():
            setattr(tag, property, value)
        return tag.render()

    def __str__(self):
        return self.render()
