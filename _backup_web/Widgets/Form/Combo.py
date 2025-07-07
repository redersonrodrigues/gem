from .Field import Field
from ...Base.Element import Element

class Combo(Field):
    """
    Representa uma combo box (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, name):
        super().__init__(name)
        self.items = None

    def addItems(self, items):
        self.items = items

    def render(self):
        tag = Element('select')
        tag.class_ = 'combo'
        tag.name = self.name
        if self.size:
            tag.style = f"width:{self.size}"
        option = Element('option')
        option.add('')
        option.value = '0'
        tag.add(option)
        if self.items:
            for chave, item in self.items.items():
                option = Element('option')
                option.value = chave
                option.add(item)
                if chave == self.value:
                    option.selected = 1
                tag.add(option)
        if not self.getEditable():
            tag.readonly = '1'
        for property, value in self.properties.items():
            setattr(tag, property, value)
        return tag.render()

    def __str__(self):
        return self.render()
