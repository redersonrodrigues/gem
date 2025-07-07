
from Lib.Escala.Widgets.Base.Element import Element


class Message(Element):
    """
    Mensagem Bootstrap 5 para interface web.
    """

    def __init__(self, type_, message):
        super().__init__('div')
        if type_ == 'info':
            self.class_ = 'alert alert-info d-flex align-items-center'
            self.role = 'alert'
            icon = Element('i')
            icon.class_ = 'fa-solid fa-circle-info me-2'
            self.add(icon)
        elif type_ == 'error':
            self.class_ = 'alert alert-danger d-flex align-items-center'
            self.role = 'alert'
            icon = Element('i')
            icon.class_ = 'fa-solid fa-circle-exclamation me-2'
            self.add(icon)
        else:
            self.class_ = 'alert alert-secondary'
            self.role = 'alert'

        self.add(message)
