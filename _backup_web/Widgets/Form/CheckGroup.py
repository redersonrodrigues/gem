from .Field import Field
from .CheckButton import CheckButton
from .Label import Label
from ...Base.Element import Element

class CheckGroup(Field):
    """
    Representa um grupo de CheckButtons (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, name):
        super().__init__(name)
        self.layout = 'vertical'
        self.items = None

    def setLayout(self, dir):
        self.layout = dir

    def addItems(self, items):
        self.items = items

    def render(self):
        html = []
        if self.items:
            for index, label in self.items.items():
                button = CheckButton(f"{self.name}[]")
                button.setValue(index)
                if self.value and index in (self.value if isinstance(self.value, (list, tuple)) else [self.value]):
                    button.setProperty('checked', '1')
                obj = Label(label)
                obj.add(button)
                html.append(str(obj))
                if self.layout == 'vertical':
                    html.append('<br>')
        return '\n'.join(html)

    def __str__(self):
        return self.render()
