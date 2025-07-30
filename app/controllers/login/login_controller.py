import hashlib
from app.models.user.user_repository import UserRepository


class LoginController:
    def __init__(self, view):
        self.view = view
        self.repo = UserRepository()

    def login(self, email, senha):
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        user = self.repo.authenticate(email, senha_hash)
        if user:
            return user  # retorna objeto User para controle de perfil/etc
        else:
            self.view.show_error("Usuário ou senha inválidos.")
            return None
