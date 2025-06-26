from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, StatementError
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.utils.logger import Logger

class EscalaRepository:
    """
    Repositório para operações CRUD e validação de escalas (plantonistas e sobreaviso).
    Centraliza regras de negócio e integridade para escalas médicas.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        """Retorna todas as escalas de plantonistas cadastradas."""
        return self.db.query(EscalaPlantonista).all()

    def get_by_id(self, escala_id: int):
        """Busca uma escala de plantonista pelo ID."""
        return self.db.query(EscalaPlantonista).filter(EscalaPlantonista.id == escala_id).first()

    def _validate(self, escala):
        """
        Valida os dados da escala antes de inserir ou atualizar.
        - Datas obrigatórias
        - Médico 1 obrigatório
        - Turno obrigatório
        """
        if not escala.data:
            raise ValueError("Data da escala é obrigatória")
        if not escala.turno:
            raise ValueError("Turno é obrigatório")
        if not escala.medico1_id:
            raise ValueError("Médico 1 é obrigatório")
        # Médico 2 é opcional

    def create(self, escala, user_id: int):
        """Cria uma nova escala após validação e registra log."""
        self._validate(escala)
        self.db.add(escala)
        self.db.commit()
        self.db.refresh(escala)
        Logger(self.db).log(user_id, 'create_escala', f'Escala ID {escala.id} criada')
        return escala

    def update(self, escala, user_id: int):
        """Atualiza uma escala existente após validação e registra log."""
        self._validate(escala)
        try:
            self.db.commit()
            self.db.refresh(escala)
            Logger(self.db).log(user_id, 'update_escala', f'Escala ID {escala.id} atualizada')
        except StatementError:
            self.db.rollback()
            raise RuntimeError("Conflito de concorrência: o registro foi modificado por outro usuário.")
        return escala

    def delete(self, escala, user_id: int):
        """Remove uma escala do banco de dados e registra log."""
        self.db.delete(escala)
        self.db.commit()
        Logger(self.db).log(user_id, 'delete_escala', f'Escala ID {escala.id} removida')
