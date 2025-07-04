from Lib.Escala.Database.record import Record

class EscalaPlantonista(Record):
    TABLENAME = "escala_plantonista"
    def __init__(self, id=None, data=None, turno=None, medico_0_id=None, medico_1_id=None):
        super().__init__(
            id=id, data=data, turno=turno,
            medico_0_id=medico_0_id, medico_1_id=medico_1_id
        )