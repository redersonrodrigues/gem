from Lib.Escala.Core.class_loader import ClassLoader
from Lib.Escala.Core.app_loader import AppLoader

# (No Python, só precisamos garantir que loaders estão disponíveis)

# Carrega o controller dinamicamente
PessoaControlClass = AppLoader.load_app_class('app.Control.PessoaControl', 'PessoaControl')
controller = PessoaControlClass()

# Simulação de parâmetros vindos de "request" (em desktop pode ser dict, em web pode ser request.args)
params = {'method': 'listar'}

controller.show(params)