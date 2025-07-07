class Field:
    """
    Representa um campo de um formulário (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, name):
        self.name = name
        self.size = None
        self.value = None
        self.editable = True
        self.formLabel = None
        self.properties = {}

    def __setattr__(self, name, value):
        if name in ('name', 'size', 'value', 'editable', 'formLabel', 'properties'):
            super().__setattr__(name, value)
        else:
            self.setProperty(name, value)

    def __getattr__(self, name):
        return self.getProperty(name)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setLabel(self, label):
        self.formLabel = label

    def getLabel(self):
        return self.formLabel

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def setEditable(self, editable):
        self.editable = editable

    def getEditable(self):
        return self.editable

    def setProperty(self, name, value):
        self.properties[name] = value

    def getProperty(self, name):
        return self.properties.get(name)

    def setSize(self, width, height=None):
        self.size = width
