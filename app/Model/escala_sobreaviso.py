from Lib.Escala.Database.record import Record

class EscalaSobreaviso(Record):
    TABLENAME = "escala_sobreaviso"
    def __init__(self, id=None, data_inicial=None, data_final=None, medico_id=None, especializacao_id=None):
        super().__init__(
            id=id, data_inicial=data_inicial, data_final=data_final,
            medico_id=medico_id, especializacao_id=especializacao_id
        )
