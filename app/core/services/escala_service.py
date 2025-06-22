"""
Service para operações de negócio envolvendo escalas médicas.
Orquestra regras de negócio, permissões e integrações entre repositórios.
"""
from app.core.escala_repository import EscalaRepository
from app.core.repositories import MedicoRepository, EspecializacaoRepository
from app.utils.permissions import can_edit

class EscalaService:
    def __init__(self, db):
        self.escala_repo = EscalaRepository(db)
        self.medico_repo = MedicoRepository(db)
        self.especializacao_repo = EspecializacaoRepository(db)
        self.db = db

    def criar_escala(self, escala, user, user_id):
        """
        Cria uma escala se o usuário tiver permissão.
        Args:
            escala: objeto Escala
            user: usuário autenticado
            user_id: id do usuário
        Returns:
            Escala criada
        Raises:
            PermissionError: se o usuário não puder editar
        """
        if not can_edit(user, escala.data):
            raise PermissionError("Usuário não tem permissão para criar escala nesta data.")
        return self.escala_repo.create(escala, user_id)

    # Outros métodos de negócio podem ser adicionados aqui (ex: atualizar, deletar, consultar)
