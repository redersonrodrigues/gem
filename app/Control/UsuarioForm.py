from Lib.Escala.Database.transaction import Transaction
from app.Model.usuario import Usuario
from app.Model.especializacao import Especializacao
from Lib.Escala.Widgets.Form import Form
from Lib.Escala.Widgets.Entry import Entry
from Lib.Escala.Widgets.Combo import Combo
from Lib.Escala.Widgets.Message import Message
from Lib.Escala.Widgets.Panel import Panel

class UsuarioForm:
    def __init__(self):
        self.form = Form('form_usuario')
        self.form.set_title('Usuário')

        # Campos do formulário
        self.id_entry = Entry('id')
        self.nome_entry = Entry('nome')
        self.login_entry = Entry('login')
        self.senha_entry = Entry('senha')
        self.perfil_combo = Combo('perfil')
        self.especializacao_combo = Combo('especializacao_id')

        # Carregar opções dos combos
        Transaction.open('escala')
        perfis = {
            'admin': 'Administrador',
            'medico': 'Médico',
            'secretaria': 'Secretaria'
        }
        self.perfil_combo.add_items(perfis)

        especializacoes = Especializacao.all()
        espec_items = {str(e.id): e.nome for e in especializacoes}
        self.especializacao_combo.add_items(espec_items)
        Transaction.close()

        # Monta o formulário
        self.form.add_field('ID', self.id_entry, '30%')
        self.form.add_field('Nome', self.nome_entry, '70%')
        self.form.add_field('Login', self.login_entry, '70%')
        self.form.add_field('Senha', self.senha_entry, '70%')
        self.form.add_field('Perfil', self.perfil_combo, '70%')
        self.form.add_field('Especialização', self.especializacao_combo, '70%')

        self.id_entry.set_editable(False)

        self.form.add_action('Salvar', self.on_save)

        self.panel = Panel()
        self.panel.add(self.form)

    def on_save(self):
        try:
            Transaction.open('escala')
            dados = self.form.get_data()
            self.form.set_data(dados)
            if dados.get('id'):
                usuario = Usuario.find(dados['id'])
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

    def on_edit(self, usuario_id):
        try:
            Transaction.open('escala')
            usuario = Usuario.find(usuario_id)
            if usuario:
                self.form.set_data(usuario.to_dict())
            Transaction.close()
        except Exception as e:
            Message('error', str(e))
            Transaction.rollback()