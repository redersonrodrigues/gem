from lib.core.entity_base import EntityBase


class User(EntityBase):
    def __init__(self, id=None, nome='', email='', senha_hash='', perfil='', ativo=True):
        super().__init__(id)
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        # 'admin', 'anestesiologista', 'admin_sistema', etc.
        self.perfil = perfil
        self.ativo = ativo

    def authenticate(self, senha_plain):
        import hashlib
        return self.senha_hash == hashlib.sha256(senha_plain.encode()).hexdigest()

    def is_admin(self):
        return self.perfil == 'admin'

    def is_anestesiologist(self):
        return self.perfil == 'anestesiologista'

    def is_system_admin(self):
        return self.perfil == 'admin_sistema'
