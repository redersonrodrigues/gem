class DatagridColumn:
    """
    Representa uma coluna de uma datagrid (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, name, label, align, width):
        self.name = name
        self.label = label
        self.align = align
        self.width = width
        self.action = None
        self.transformer = None

    def getName(self):
        return self.name

    def getLabel(self):
        return self.label

    def getAlign(self):
        return self.align

    def getWidth(self):
        return self.width

    def setAction(self, action):
        self.action = action

    def getAction(self):
        if self.action:
            return self.action.serialize() if hasattr(self.action, 'serialize') else self.action

    def setTransformer(self, callback):
        self.transformer = callback

    def getTransformer(self):
        return self.transformer
