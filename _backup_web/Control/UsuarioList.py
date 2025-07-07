from Lib.Escala.Database.transaction import Transaction
from Lib.Escala.Database.repository import Repository
from Lib.Escala.Database.criteria import Criteria
from app.Model.usuario import Usuario
from app.Control.UsuarioForm import UsuarioForm
from Lib.Escala.Widgets.Form import Form
from Lib.Escala.Widgets.Entry import Entry
from Lib.Escala.Widgets.Container import VBox
from Lib.Escala.Widgets.Datagrid import Datagrid
from Lib.Escala.Widgets.DatagridColumn import DatagridColumn
from Lib.Escala.Widgets.Dialog import Message, Question
from Lib.Escala.Widgets.Container import Panel
from Lib.Escala.Widgets.Wrapper import FormWrapper, DatagridWrapper

class UsuarioList:
    def __init__(self):
        # Formulário de busca
        self.form = FormWrapper(Form('form_busca_usuarios'))
        self.form.set_title('Usuários')

        self.nome_entry = Entry('nome')
        self.form.add_field('Nome', self.nome_entry, '100%')
        self.form.add_action('Buscar', self.on_reload)
        self.form.add_action('Novo', lambda: UsuarioForm().on_edit(None))

        # Datagrid
        self.datagrid = DatagridWrapper(Datagrid())

        # Colunas da datagrid
        col_id = DatagridColumn('id', 'ID', 'center', '10%')
        col_nome = DatagridColumn('nome', 'Nome', 'left', '40%')
        col_login = DatagridColumn('login', 'Login', 'left', '30%')
        col_perfil = DatagridColumn('perfil', 'Perfil', 'left', '20%')

        self.datagrid.add_column(col_id)
        self.datagrid.add_column(col_nome)
        self.datagrid.add_column(col_login)
        self.datagrid.add_column(col_perfil)

        # Ações da datagrid
        self.datagrid.add_action('Editar', lambda item: UsuarioForm().on_edit(item.id), 'id', 'fa fa-edit fa-lg blue')
        self.datagrid.add_action('Excluir', self.on_delete, 'id', 'fa fa-trash fa-lg red')

        # Monta página
        self.box = VBox()
        self.box.style = 'display:block'
        self.box.add(self.form)
        self.box.add(self.datagrid)

        self.loaded = False

    def on_reload(self, *args, **kwargs):
        Transaction.open('escala')
        repository = Repository(Usuario)
        criteria = Criteria()
        criteria.set_property('order', 'id')

        dados = self.form.get_data()
        if dados.get('nome'):
            criteria.add('nome', 'like', f"%{dados['nome']}%")

        usuarios = repository.load(criteria)
        self.datagrid.clear()
        if usuarios:
            for usuario in usuarios:
                self.datagrid.add_item(usuario)
        Transaction.close()
        self.loaded = True

    def on_delete(self, id):
        action1 = lambda: self.delete({'id': id})
        Question('Deseja realmente excluir o registro?', action1)

    def delete(self, param):
        try:
            id = param['id']
            Transaction.open('escala')
            usuario = Usuario.find(id)
            if usuario:
                usuario.delete()
            Transaction.close()
            self.on_reload()
            Message('info', 'Registro excluído com sucesso')
        except Exception as e:
            Message('error', str(e))

    def show(self):
        if not self.loaded:
            self.on_reload()
        # Aqui você deve adicionar lógica para exibir self.box em sua framework/view principal