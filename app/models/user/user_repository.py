from app.models.user.user import User
from lib.db.repository import Repository
from app.models.user.user_mapper import UserMapper


class UserRepository(Repository):
    def __init__(self):
        super().__init__(User)
        self.mapper = UserMapper()

    def authenticate(self, email, senha_hash):
        # Consulta ao banco, retorna User se achou e está ativo.
        query = "SELECT * FROM user WHERE email=:email AND senha_hash=:senha_hash AND ativo=1"
        row = self.adapter.fetchone(
            query, {"email": email, "senha_hash": senha_hash})
        if row:
            return self.mapper.to_entity(row)
        return None
