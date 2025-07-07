from ..Container.Panel import Panel
from ..Form.Form import Form
from ..Form.Button import Button
from ...Base.Element import Element

class FormWrapper:
    """
    Decora formulários no formato Bootstrap (adaptado de Pablo Dall'Oglio)
    """
    def __init__(self, form):
        self.decorated = form

    def __getattr__(self, name):
        return getattr(self.decorated, name)

    def render(self):
        element = Element('form')
        element.class_ = 'form-horizontal'
        element.enctype = 'multipart/form-data'
        element.method = 'post'
        element.name = self.decorated.getName()
        element.width = '100%'
        for field in self.decorated.getFields().values():
            group = Element('div')
            group.class_ = 'form-group'
            label = Element('label')
            label.class_ = 'col-sm-2 control-label'
            label.add(field.getLabel())
            col = Element('div')
            col.class_ = 'col-sm-10'
            col.add(field)
            field.class_ = 'form-control'
            group.add(label)
            group.add(col)
            element.add(group)
        footer = Element('div')
        i = 0
        for label, action in self.decorated.getActions().items():
            name = label.lower().replace(' ', '_')
            button = Button(name)
            button.setFormName(self.decorated.getName())
            button.setAction(action, label)
            button.class_ = 'btn ' + ('btn-success' if i == 0 else 'btn-default')
            footer.add(button)
            i += 1
        panel = Panel(self.decorated.getTitle())
        panel.add(element)
        panel.addFooter(footer)
        return str(panel)

    def __str__(self):
        return self.render()
