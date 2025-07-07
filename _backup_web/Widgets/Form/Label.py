from .Field import Field
from ...Base.Element import Element

class Label(Field):
    """
    Representa um rótulo de texto (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, value):
        super().__init__(None)
        self.setValue(value)
        self.tag = Element('label')

    def add(self, child):
        self.tag.add(child)

    def render(self):
        self.tag.add(self.value)
        return self.tag.render()

    def __str__(self):
        return self.render()
