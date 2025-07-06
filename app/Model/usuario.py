class Usuario:
    TABLENAME = "usuario"

    _db = [
        {"id": 1, "nome": "João", "login": "joao",
            "senha_hash": "1234", "perfil": "admin", "status": 1},
        {"id": 2, "nome": "Maria", "login": "maria",
            "senha_hash": "abcd", "perfil": "medico", "status": 1},
        {"id": 3, "nome": "Carlos", "login": "carlos",
            "senha_hash": "xyz", "perfil": "secretaria", "status": 1}
    ]
    _next_id = 4

    def __init__(self, id=None, nome=None, login=None, senha_hash=None, perfil=None, status=None):
        self.id = id
        self.nome = nome
        self.login = login
        self.senha_hash = senha_hash
        self.perfil = perfil
        self.status = status

    @staticmethod
    def find(id):
        for u in Usuario._db:
            if u["id"] == id:
                return Usuario(**u)
        return None

    @staticmethod
    def all():
        return [Usuario(**u) for u in Usuario._db]

    def store(self):
        if self.id is None:
            self.id = Usuario._next_id
            Usuario._next_id += 1
            Usuario._db.append(self.to_dict())
        else:
            for u in Usuario._db:
                if u["id"] == self.id:
                    u.update(self.to_dict())
                    break

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "login": self.login,
            "senha_hash": self.senha_hash,
            "perfil": self.perfil,
            "status": self.status
        }

    def delete(self):
        Usuario._db = [u for u in Usuario._db if u["id"] != self.id]

    def load(self, id):
        u = Usuario.find(id)
        if u:
            self.id = u.id
            self.nome = u.nome
            self.login = u.login
            self.senha_hash = u.senha_hash
            self.perfil = u.perfil
            self.status = u.status
            return self
        return None
