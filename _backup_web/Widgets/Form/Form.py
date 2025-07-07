class Form:
    """
    Representa um formulário (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, name='my_form'):
        self.setName(name)
        self.fields = {}
        self.actions = {}
        self.title = None

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setTitle(self, title):
        self.title = title

    def getTitle(self):
        return self.title

    def addField(self, label, obj, size='100%'):
        obj.setSize(size)
        obj.setLabel(label)
        self.fields[obj.getName()] = obj

    def addAction(self, label, action):
        self.actions[label] = action

    def getFields(self):
        return self.fields

    def getActions(self):
        return self.actions

    def setData(self, obj):
        for name, field in self.fields.items():
            if name and hasattr(obj, name):
                field.setValue(getattr(obj, name))

    def getData(self, cls=dict, post_data=None, files_data=None):
        data = cls()
        post_data = post_data or {}
        files_data = files_data or {}
        for key, field in self.fields.items():
            val = post_data.get(key, '')
            if isinstance(data, dict):
                data[key] = val
            else:
                setattr(data, key, val)
        for key, content in files_data.items():
            if isinstance(data, dict):
                data[key] = content.get('tmp_name', '')
            else:
                setattr(data, key, content.get('tmp_name', ''))
        return data
