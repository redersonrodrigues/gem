from .Field import Field
from ...Base.Element import Element

class RadioButton(Field):
    """
    Representa um RadioButton (adaptado de Pablo Dall'Oglio)
    """
    def render(self):
        tag = Element('input')
        tag.class_ = 'field'
        tag.name = self.name
        tag.value = self.value
        tag.type = 'radio'
        if not self.getEditable():
            tag.readonly = '1'
        for property, value in self.properties.items():
            setattr(tag, property, value)
        return tag.render()

    def __str__(self):
        return self.render()
