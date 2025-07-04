from Lib.Escala.Database.record import Record

class Especializacao(Record):
    TABLENAME = "especializacao"

    def __init__(self, id=None, nome=None):
        super().__init__(
            id=id,
            nome=nome
        )