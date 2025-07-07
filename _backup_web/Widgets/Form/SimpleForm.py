class SimpleForm:
    """
    Um formulário simples inspirado no exemplo de Pablo Dall'Oglio.
    Permite definir nome, título, campos e ação, e renderiza o HTML (Bootstrap compatível).
    """

    def __init__(self, name):
        self.name = name
        self.fields = []
        self.title = ''
        self.action = ''

    def set_title(self, title):
        self.title = title

    def add_field(self, label, name, field_type, value, css_class=''):
        self.fields.append({
            'label': label,
            'name': name,
            'type': field_type,
            'value': value,
            'class': css_class,
        })

    def set_action(self, action):
        self.action = action

    def render(self):
        html = []
        html.append("<div class='panel panel-default' style='margin: 40px;'>")
        html.append(f"<div class='panel-heading'> {self.title} </div>")
        html.append("<div class='panel-body'>")
        html.append(f"<form method='POST' action='{self.action}' class='form-horizontal'>")
        if self.fields:
            for field in self.fields:
                html.append("<div class='form-group'>")
                html.append(f"<label class='col-sm-2 control-label'> {field['label']} </label>")
                html.append("<div class='col-sm-10'>")
                html.append(
                    f"<input type='{field['type']}' name='{field['name']}' "
                    f"value='{field['value']}' class='{field['class']}'>"
                )
                html.append("</div>")
                html.append("</div>")
            html.append("<div class='form-group'>")
            html.append("<div class='col-sm-offset-2 col-sm-8'>")
            html.append("<input type='submit' class='btn btn-success' value='enviar'>")
            html.append("</div>")
            html.append("</div>")
        html.append("</form>")
        html.append("</div>")
        html.append("</div>")
        return "\n".join(html)