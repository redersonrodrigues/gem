from Lib.Escala.Control.Page import Page
from Lib.Escala.Control.action import Action
from Lib.Escala.Widgets.Form.Form import Form
from Lib.Escala.Widgets.Form.Entry import Entry
from Lib.Escala.Widgets.Form.Combo import Combo
from Lib.Escala.Widgets.Dialog.Message import Message
from Lib.Escala.Database.transaction import Transaction
from Lib.Escala.Widgets.Container.Panel import Panel
from Lib.Escala.Widgets.Wrapper.FormWrapper import FormWrapper
from app.Model.Usuario import Usuario
from app.Model.especializacao import Especializacao

class UsuarioForm(Page):
    def __init__(self):
        super().__init__()
        # Use FormWrapper para padronizar
        self.form = FormWrapper(Form('form_usuario'))
        self.form.set_title('Usuário')

        # Campos do formulário
        codigo = Entry('id')
        nome = Entry('nome')
        login = Entry('login')
        senha = Entry('senha')
        perfil = Combo('perfil')
        especializacao = Combo('especializacao_id')

        # Carregar opções dos combos
        try:
            Transaction.open('escala')
            perfis = {
                'admin': 'Administrador',
                'medico': 'Médico',
                'secretaria': 'Secretaria'
            }
            perfil.add_items(perfis)

            especializacoes = Especializacao.all()
            espec_items = {str(e.id): e.nome for e in especializacoes}
            especializacao.add_items(espec_items)
            Transaction.close()
        except Exception as e:
            Message('error', str(e))
            Transaction.rollback()

        # Monta o formulário
        self.form.add_field('ID', codigo, '30%')
        self.form.add_field('Nome', nome, '70%')
        self.form.add_field('Login', login, '70%')
        self.form.add_field('Senha', senha, '70%')
        self.form.add_field('Perfil', perfil, '70%')
        self.form.add_field('Especialização', especializacao, '70%')

        codigo.set_editable(False)

        # Adiciona ação 'Salvar' usando Action
        self.form.add_action('Salvar', Action(self.on_save))

        # Adiciona o formulário na página/painel
        super().add(self.form)

    def on_save(self, param=None):
        try:
            Transaction.open('escala')
            dados = self.form.get_data()
            self.form.set_data(dados)
            if hasattr(dados, 'id') and dados.id:
                usuario = Usuario.find(dados.id)
                if not usuario:
                    usuario = Usuario()
            else:
                usuario = Usuario()
            usuario.from_dict(dados)
            usuario.store()
            Transaction.close()
            Message('info', 'Usuário salvo com sucesso!')
        except Exception as e:
            Message('error', str(e))
            Transaction.rollback()

    def on_edit(self, param):
        try:
            if 'id' in param:
                usuario_id = param['id']
                Transaction.open('escala')
                usuario = Usuario.find(usuario_id)
                if usuario:
                    self.form.set_data(usuario.to_dict())
                Transaction.close()
        except Exception as e:
            Message('error', str(e))
            Transaction.rollback()