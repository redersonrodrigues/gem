"""
Implementação do padrão Repository para abstração de acesso ao banco de dados.
Cada entidade terá seu próprio repositório, facilitando testes, manutenção e futuras migrações.
"""
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError
from typing import Generic, TypeVar, Type, List, Optional
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[T]:
        return db.query(self.model).get(id)

    def list(self, db: Session) -> List[T]:
        return db.query(self.model).all()

    def add(self, db: Session, obj: T) -> T:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: T) -> T:
        try:
            db.commit()
            db.refresh(obj)
        except StaleDataError:
            db.rollback()
            raise RuntimeError("Conflito de concorrência: o registro foi modificado por outro usuário.")
        return obj

    def delete(self, db: Session, obj: T) -> None:
        db.delete(obj)
        db.commit()

# Repositórios específicos
class MedicoRepository(BaseRepository[Medico]):
    def __init__(self):
        super().__init__(Medico)

class EspecializacaoRepository(BaseRepository[Especializacao]):
    def __init__(self):
        super().__init__(Especializacao)

class EscalaPlantonistaRepository(BaseRepository[EscalaPlantonista]):
    def __init__(self):
        super().__init__(EscalaPlantonista)

class EscalaSobreavisoRepository(BaseRepository[EscalaSobreaviso]):
    def __init__(self):
        super().__init__(EscalaSobreaviso)
