from Lib.Escala.Control.Page import Page
from app.Model.Usuario import Usuario

class UsuarioControl(Page):
    def listar(self, param=None):
        try:
            usuarios = Usuario.all()
            html = "<h2>Lista de Usuários</h2><ul>"
            for usuario in usuarios:
                html += f"<li>{usuario.id} - {usuario.nome}</li>"
            html += "</ul>"
            return html
        except Exception as e:
            return f"<h3>Erro ao listar usuários: {e}</h3>"