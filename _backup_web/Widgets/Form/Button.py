from .Field import Field
from ...Base.Element import Element

class Button(Field):
    """
    Representa um botão (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, name):
        super().__init__(name)
        self.action = None
        self.label = None
        self.formName = None

    def setAction(self, action, label):
        self.action = action
        self.label = label

    def setFormName(self, name):
        self.formName = name

    def render(self):
        url = self.action.serialize() if self.action and hasattr(self.action, 'serialize') else '#'
        tag = Element('button')
        tag.name = self.name
        tag.type = 'button'
        tag.add(self.label)
        tag.onclick = f"document.{self.formName}.action='{url}'; document.{self.formName}.submit()"
        for property, value in self.properties.items():
            setattr(tag, property, value)
        return tag.render()

    def __str__(self):
        return self.render()
