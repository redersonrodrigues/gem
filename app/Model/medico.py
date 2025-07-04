from Lib.Escala.Database.record import Record

class Medico(Record):
    TABLENAME = "medico"

    def __init__(
        self,
        id=None,
        nome=None,
        nome_pj=None,
        especializacao_id=None,
        status=None
    ):
        super().__init__(
            id=id,
            nome=nome,
            nome_pj=nome_pj,
            especializacao_id=especializacao_id,
            status=status
        )