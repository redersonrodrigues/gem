from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import StaleDataError
from app.models import Medico, Especializacao
from app.utils.cache import cache

class MedicoRepository:
    """Repositório para operações CRUD e validação de médicos."""
    def __init__(self, db: Session):
        """Inicializa o repositório com a sessão do banco de dados."""
        self.db = db

    def get_all(self):
        """Retorna todos os médicos cadastrados (objetos ORM), usando cache local."""
        cached = cache.get('medicos')
        if cached is not None:
            return cached
        result = self.db.query(Medico).all()
        cache.set('medicos', result)
        return result

    def get_by_id(self, medico_id: int):
        """Busca um médico pelo ID."""
        return self.db.query(Medico).filter(Medico.id == medico_id).first()

    def _validate(self, medico: Medico):
        """
        Valida os dados do médico antes de inserir ou atualizar.
        - Nome não pode ser vazio
        - Especialização obrigatória e existente
        - Status deve ser um valor permitido
        """
        if not medico.nome or not medico.nome.strip():
            raise ValueError("nome do médico é obrigatório")
        if medico.especializacao_id is None:
            raise ValueError("Especialização não encontrada")
        # Checagem de especialização existente
        if not self.db.query(Especializacao).filter(Especializacao.id == medico.especializacao_id).first():
            raise ValueError("Especialização não encontrada")
        # Checagem de status válido
        from app.models.medico import StatusMedicoEnum
        status_values = [e.value for e in StatusMedicoEnum]
        if medico.status not in status_values:
            raise ValueError("Status inválido")

    def create(self, medico: Medico):
        """Cria um novo médico após validação."""
        self._validate(medico)
        self.db.add(medico)
        self.db.commit()
        self.db.refresh(medico)
        cache.invalidate('medicos')
        return medico

    def update(self, medico: Medico):
        """Atualiza um médico existente após validação."""
        self._validate(medico)
        try:
            self.db.commit()
            self.db.refresh(medico)
        except StaleDataError:
            self.db.rollback()
            raise RuntimeError("Conflito de concorrência: o registro foi modificado por outro usuário.")
        cache.invalidate('medicos')
        return medico

    def delete(self, medico: Medico):
        """Remove um médico do banco de dados."""
        self.db.delete(medico)
        self.db.commit()
        cache.invalidate('medicos')

class EspecializacaoRepository:
    """Repositório para operações CRUD e validação de especializações."""
    def __init__(self, db: Session):
        """Inicializa o repositório com a sessão do banco de dados."""
        self.db = db

    def get_all(self):
        """Retorna todas as especializações cadastradas, usando cache local."""
        cached = cache.get('especializacoes')
        if cached is not None:
            return cached
        result = self.db.query(Especializacao).all()
        cache.set('especializacoes', result)
        return result

    def get_by_id(self, especializacao_id: int):
        """Busca uma especialização pelo ID."""
        return self.db.query(Especializacao).filter(Especializacao.id == especializacao_id).first()

    def _validate(self, especializacao: Especializacao):
        """
        Valida os dados da especialização antes de inserir ou atualizar.
        - Nome não pode ser vazio
        """
        if not especializacao.nome or not especializacao.nome.strip():
            raise ValueError("nome da especialização é obrigatório")

    def create(self, especializacao: Especializacao):
        """Cria uma nova especialização após validação."""
        self._validate(especializacao)
        self.db.add(especializacao)
        self.db.commit()
        self.db.refresh(especializacao)
        cache.invalidate('especializacoes')
        return especializacao

    def update(self, especializacao: Especializacao):
        """Atualiza uma especialização existente após validação."""
        self._validate(especializacao)
        try:
            self.db.commit()
            self.db.refresh(especializacao)
        except StaleDataError:
            self.db.rollback()
            raise RuntimeError("Conflito de concorrência: o registro foi modificado por outro usuário.")
        cache.invalidate('especializacoes')
        return especializacao

    def delete(self, especializacao: Especializacao):
        """Remove uma especialização do banco de dados."""
        self.db.delete(especializacao)
        self.db.commit()
        cache.invalidate('especializacoes')
