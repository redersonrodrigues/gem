from .Field import Field
from ...Base.Element import Element

class File(Field):
    """
    Representa um componente de upload de arquivo (adaptado de Pablo Dall'Oglio)
    """
    def render(self):
        tag = Element('input')
        tag.class_ = 'field'
        tag.name = self.name
        tag.value = self.value
        tag.type = 'file'
        if self.size:
            tag.style = f"width:{self.size}"
        if not self.getEditable():
            tag.readonly = '1'
        for property, value in self.properties.items():
            setattr(tag, property, value)
        return tag.render()

    def __str__(self):
        return self.render()
