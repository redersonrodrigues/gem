from Lib.Escala.Widgets.Base.Element import Element


class Question(Element):
    """
    Exibe uma pergunta ao usuário com botões de confirmação e negação.
    """

    def __init__(self, message, action_yes, action_no=None):
        super().__init__('div')
        # Bootstrap 5 alert-warning
        self.class_ = 'alert alert-warning question d-flex align-items-center justify-content-between gap-2'
        self.role = 'alert'

        # Texto da pergunta
        msg = Element('span')
        msg.add(message)

        # Botão Sim
        btn_yes = Element('a')
        btn_yes.class_ = 'btn btn-primary ms-2'
        btn_yes.href = action_yes.serialize()
        btn_yes.add('Sim')

        # Botão Não (opcional)
        if action_no:
            btn_no = Element('a')
            btn_no.class_ = 'btn btn-secondary ms-2'
            btn_no.href = action_no.serialize()
            btn_no.add('Não')
            btn_group = Element('div')
            btn_group.class_ = 'd-flex gap-2'
            btn_group.add(btn_yes)
            btn_group.add(btn_no)
        else:
            btn_group = btn_yes

        # Montagem do diálogo
        self.add(msg)
        self.add(btn_group)
