from abc import ABC, abstractmethod
from Lib.Escala.Database.repository import Repository

class EscalaStrategy(ABC):
    @abstractmethod
    def criar_escala(self, **kwargs):
        pass

    @abstractmethod
    def buscar_escala(self, **kwargs):
        pass
from Lib.Escala.Database.criteria import Criteria
from app.Model.escala_plantonista import EscalaPlantonista
from app.Model.escala_sobreaviso import EscalaSobreaviso

class EscalaPlantonistaStrategy(EscalaStrategy):
    def criar_escala(self, **kwargs):
        escala = EscalaPlantonista(
            data=kwargs["data"], turno=kwargs["turno"],
            medico_0_id=kwargs["medico_0_id"], medico_1_id=kwargs["medico_1_id"]
        )
        escala.store()
        return escala

    def buscar_escala(self, **kwargs):
        c = Criteria()
        if "data" in kwargs:
            c.add("data", "=", kwargs["data"])
        if "turno" in kwargs:
            c.add("turno", "=", kwargs["turno"])
        repo = Repository(EscalaPlantonista)
        return repo.load(c)

class EscalaSobreavisoStrategy(EscalaStrategy):
    def criar_escala(self, **kwargs):
        escala = EscalaSobreaviso(
            data_inicial=kwargs["data_inicial"],
            data_final=kwargs["data_final"],
            medico_id=kwargs["medico_id"],
            especializacao_id=kwargs["especializacao_id"]
        )
        escala.store()
        return escala

    def buscar_escala(self, **kwargs):
        c = Criteria()
        if "data" in kwargs:
            c.add("data_inicial", "<=", kwargs["data"])
            c.add("data_final", ">=", kwargs["data"])
        repo = Repository(EscalaSobreaviso)
        return repo.load(c)