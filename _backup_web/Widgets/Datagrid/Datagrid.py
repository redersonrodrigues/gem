class Datagrid:
    """
    Representa uma Datagrid (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self):
        self.columns = []
        self.items = []
        self.actions = []

    def addColumn(self, column):
        self.columns.append(column)

    def addAction(self, label, action, field, image=None):
        self.actions.append({
            'label': label,
            'action': action,
            'field': field,
            'image': image
        })

    def addItem(self, obj):
        self.items.append(obj)
        for column in self.columns:
            name = column.getName()
            if not hasattr(obj, name):
                getattr(obj, name, None)

    def getColumns(self):
        return self.columns

    def getItems(self):
        return self.items

    def getActions(self):
        return self.actions

    def clear(self):
        self.items = []
