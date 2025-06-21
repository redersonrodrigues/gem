from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Medico, Especializacao, Escala

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

class EscalaRepository:
    """Repositório para operações CRUD e validação de escalas."""
    def __init__(self, db: Session):
        """Inicializa o repositório com a sessão do banco de dados."""
        self.db = db

    def get_all(self):
        """Retorna todas as escalas cadastradas."""
        return self.db.query(Escala).all()

    def get_by_id(self, escala_id: int):
        """Busca uma escala pelo ID."""
        return self.db.query(Escala).filter(Escala.id == escala_id).first()

    def _validate(self, escala: Escala):
        """Valida os dados da escala antes de inserir ou atualizar."""
        if escala.medico_id is None:
            raise ValueError("O médico é obrigatório na escala.")
        if not escala.dia_da_semana:
            raise ValueError("O dia da semana é obrigatório na escala.")
        # Checagem de médico existente
        if not self.db.query(Medico).filter(Medico.id == escala.medico_id).first():
            raise ValueError("Médico não encontrado para a escala.")

    def create(self, escala: Escala):
        """Cria uma nova escala após validação."""
        self._validate(escala)
        self.db.add(escala)
        self.db.commit()
        self.db.refresh(escala)
        return escala

    def update(self, escala: Escala):
        """Atualiza uma escala existente após validação."""
        self._validate(escala)
        self.db.commit()
        self.db.refresh(escala)
        return escala

    def delete(self, escala: Escala):
        """Remove uma escala do banco de dados."""
        self.db.delete(escala)
        self.db.commit()
