from Lib.Escala.Widgets.Form.SimpleForm import SimpleForm

class SimpleFormControl:
    def __init__(self):
        self.form = SimpleForm('my_form')
        self.form.set_title('Pessoa')
        self.form.add_field('Nome', 'name', 'text', 'Maria', 'form-control')
        self.form.add_field('Endereço', 'endereco', 'text', 'Rua das flores', 'form-control')
        self.form.add_field('Telefone', 'fone', 'text', '(51) 1234-5678', 'form-control')
        self.form.set_action('index.py?class=SimpleFormControl&method=onGravar')
        self.html = self.form.show()

    def onGravar(self, params):
        # Aqui você trataria os dados do POST
        pass