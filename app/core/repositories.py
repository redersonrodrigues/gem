from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Medico, Especializacao, Escala

class MedicoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Medico).all()

    def get_by_id(self, medico_id: int):
        return self.db.query(Medico).filter(Medico.id == medico_id).first()

    def _validate(self, medico: Medico):
        if not medico.nome:
            raise ValueError("O nome do médico é obrigatório.")
        if not medico.crm:
            raise ValueError("O CRM do médico é obrigatório.")
        if medico.especialidade_id is None:
            raise ValueError("A especialidade é obrigatória.")
        # Unicidade do CRM
        query = self.db.query(Medico).filter(Medico.crm == medico.crm)
        if medico.id:
            query = query.filter(Medico.id != medico.id)
        if query.first():
            raise ValueError("Já existe um médico com este CRM.")
        # Checagem de especialidade existente
        if not self.db.query(Especializacao).filter(Especializacao.id == medico.especialidade_id).first():
            raise ValueError("Especialidade não encontrada.")

    def create(self, medico: Medico):
        self._validate(medico)
        self.db.add(medico)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def update(self, medico: Medico):
        self._validate(medico)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def delete(self, medico: Medico):
        self.db.delete(medico)
        self.db.commit()

class EspecializacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Especializacao).all()

    def get_by_id(self, especializacao_id: int):
        return self.db.query(Especializacao).filter(Especializacao.id == especializacao_id).first()

    def _validate(self, especializacao: Especializacao):
        if not especializacao.nome:
            raise ValueError("O nome da especialização é obrigatório.")

    def create(self, especializacao: Especializacao):
        self._validate(especializacao)
        self.db.add(especializacao)
        self.db.commit()
        self.db.refresh(especializacao)
        return especializacao

    def update(self, especializacao: Especializacao):
        self._validate(especializacao)
        self.db.commit()
        self.db.refresh(especializacao)
        return especializacao

    def delete(self, especializacao: Especializacao):
        self.db.delete(especializacao)
        self.db.commit()

class EscalaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Escala).all()

    def get_by_id(self, escala_id: int):
        return self.db.query(Escala).filter(Escala.id == escala_id).first()

    def _validate(self, escala: Escala):
        if escala.medico_id is None:
            raise ValueError("O médico é obrigatório na escala.")
        if not escala.dia_da_semana:
            raise ValueError("O dia da semana é obrigatório na escala.")
        # Checagem de médico existente
        if not self.db.query(Medico).filter(Medico.id == escala.medico_id).first():
            raise ValueError("Médico não encontrado para a escala.")

    def create(self, escala: Escala):
        self._validate(escala)
        self.db.add(escala)
        self.db.commit()
        self.db.refresh(escala)
        return escala

    def update(self, escala: Escala):
        self._validate(escala)
        self.db.commit()
        self.db.refresh(escala)
        return escala

    def delete(self, escala: Escala):
        self.db.delete(escala)
        self.db.commit()
