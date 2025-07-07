class Action:
    def __init__(self, obj, method):
        self.obj = obj
        self.method = method
        self.param = {}

    def set_parameter(self, name, value):
        self.param[name] = value

    def serialize(self):
        # Monta URL do tipo ?class=Classe&method=metodo&param1=valor1...
        params = {'class': self.obj.__class__.__name__, 'method': self.method}
        params.update(self.param)
        # Exemplo: ?class=ExemploQuestionControl&method=onConfirma&codigo=1200
        return '?' + '&'.join(f'{k}={v}' for k, v in params.items())