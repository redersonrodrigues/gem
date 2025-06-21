from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Medico, Especializacao

class MedicoRepository:
    """Repositório para operações CRUD e validação de médicos."""
    def __init__(self, db: Session):
        """Inicializa o repositório com a sessão do banco de dados."""
        self.db = db

    def get_all(self):
        """Retorna todos os médicos cadastrados."""
        return self.db.query(Medico).all()

    def get_by_id(self, medico_id: int):
        """Busca um médico pelo ID."""
        return self.db.query(Medico).filter(Medico.id == medico_id).first()

    def _validate(self, medico: Medico):
        """Valida os dados do médico antes de inserir ou atualizar."""
        if not medico.nome:
            raise ValueError("O nome do médico é obrigatório.")
        if medico.especializacao_id is None:
            raise ValueError("A especialização é obrigatória.")
        # Checagem de especialização existente
        if not self.db.query(Especializacao).filter(Especializacao.id == medico.especializacao_id).first():
            raise ValueError("Especialização não encontrada.")

    def create(self, medico: Medico):
        """Cria um novo médico após validação."""
        self._validate(medico)
        self.db.add(medico)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def update(self, medico: Medico):
        """Atualiza um médico existente após validação."""
        self._validate(medico)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def delete(self, medico: Medico):
        """Remove um médico do banco de dados."""
        self.db.delete(medico)
        self.db.commit()

class EspecializacaoRepository:
    """Repositório para operações CRUD e validação de especializações."""
    def __init__(self, db: Session):
        """Inicializa o repositório com a sessão do banco de dados."""
        self.db = db

    def get_all(self):
        """Retorna todas as especializações cadastradas."""
        return self.db.query(Especializacao).all()

    def get_by_id(self, especializacao_id: int):
        """Busca uma especialização pelo ID."""
        return self.db.query(Especializacao).filter(Especializacao.id == especializacao_id).first()

    def _validate(self, especializacao: Especializacao):
        """Valida os dados da especialização antes de inserir ou atualizar."""
        if not especializacao.nome:
            raise ValueError("O nome da especialização é obrigatório.")

    def create(self, especializacao: Especializacao):
        """Cria uma nova especialização após validação."""
        self._validate(especializacao)
        self.db.add(especializacao)
        self.db.commit()
        self.db.refresh(especializacao)
        return especializacao

    def update(self, especializacao: Especializacao):
        """Atualiza uma especialização existente após validação."""
        self._validate(especializacao)
        self.db.commit()
        self.db.refresh(especializacao)
        return especializacao

    def delete(self, especializacao: Especializacao):
        """Remove uma especialização do banco de dados."""
        self.db.delete(especializacao)
        self.db.commit()
