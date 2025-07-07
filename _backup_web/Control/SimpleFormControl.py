from Lib.Escala.Control.Page import Page
from Lib.Escala.Widgets.Form.SimpleForm import SimpleForm


class SimpleFormControl(Page):
    def __init__(self):
        super().__init__()
        self.form = SimpleForm('my_form')
        self.form.set_title('Título')
        self.form.add_field('Nome', 'nome', 'text', 'Maria', 'form-control')
        self.form.add_field('Endereço', 'endereco', 'text',
                            'Rua das flores', 'form-control')
        self.form.add_field('Telefone', 'telefone', 'text',
                            '(51) 1234-5678', 'form-control')
        # Define ação apontando para o Front Controller, passando parâmetros da classe e método
        self.form.set_action('?class=SimpleFormControl&method=onGravar')

    def show(self, param=None):
        # Exibe o formulário (chamado pelo Front Controller)
        return self.form.render()

    def onGravar(self, param):
        # Exibe os dados recebidos via POST (simulação)
        return f"<pre>{param}</pre>"
