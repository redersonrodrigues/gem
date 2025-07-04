from Lib.Escala.Database.record import Record

class Usuario(Record):
    TABLENAME = "usuario"

    def __init__(self, id=None, nome=None, login=None, senha_hash=None, perfil=None, status=None):
        # O super().__init__ aceita id, mas também já permite setar outros campos via kwargs
        super().__init__(id=id, nome=nome, login=login, senha_hash=senha_hash, perfil=perfil, status=status)