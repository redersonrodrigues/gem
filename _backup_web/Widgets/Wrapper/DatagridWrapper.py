from ..Container.Panel import Panel
from ..Datagrid.Datagrid import Datagrid
from ...Base.Element import Element

class DatagridWrapper:
    """
    Decora datagrids no formato Bootstrap (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, datagrid):
        self.decorated = datagrid

    def __getattr__(self, name):
        return getattr(self.decorated, name)

    def __setattr__(self, name, value):
        if name == 'decorated':
            super().__setattr__(name, value)
        else:
            setattr(self.decorated, name, value)

    def render(self):
        element = Element('table')
        element.class_ = 'table table-striped table-hover'
        thead = Element('thead')
        element.add(thead)
        self.createHeaders(thead)
        tbody = Element('tbody')
        element.add(tbody)
        items = self.decorated.getItems()
        for item in items:
            self.createItem(tbody, item)
        panel = Panel()
        panel.type = 'datagrid'
        panel.add(element)
        return str(panel)

    def createHeaders(self, thead):
        row = Element('tr')
        thead.add(row)
        actions = self.decorated.getActions()
        columns = self.decorated.getColumns()
        if actions:
            for _ in actions:
                celula = Element('th')
                celula.width = '40px'
                row.add(celula)
        if columns:
            for column in columns:
                label = column.getLabel()
                align = column.getAlign()
                width = column.getWidth()
                celula = Element('th')
                celula.add(label)
                celula.style = f'text-align:{align}'
                celula.width = width
                row.add(celula)
                if column.getAction():
                    url = column.getAction()
                    celula.onclick = f"document.location='{url}'"

    def createItem(self, tbody, item):
        row = Element('tr')
        tbody.add(row)
        actions = self.decorated.getActions()
        columns = self.decorated.getColumns()
        if actions:
            for action in actions:
                url = action['action'].serialize() if hasattr(action['action'], 'serialize') else '#'
                label = action['label']
                image = action['image']
                field = action['field']
                key = getattr(item, field, None)
                link = Element('a')
                link.href = f"{url}&key={key}&{field}={key}"
                if image:
                    i = Element('i')
                    i.class_ = image
                    i.title = label
                    i.add('')
                    link.add(i)
                else:
                    link.add(label)
                element = Element('td')
                element.add(link)
                element.align = 'center'
                row.add(element)
        if columns:
            for column in columns:
                name = column.getName()
                align = column.getAlign()
                width = column.getWidth()
                function = column.getTransformer()
                data = getattr(item, name, '')
                if function:
                    data = function(data)
                element = Element('td')
                element.add(data)
                element.align = align
                element.width = width
                row.add(element)

    def __str__(self):
        return self.render()
