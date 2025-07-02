# Serviço para gerenciamento de médicos
from typing import List, Optional
from gem.repositories.medico_repository import MedicoRepository
from gem.models.base_models import Medico


class MedicoService:
    """Serviço para lógica de negócio relacionada a médicos"""
    
    def __init__(self):
        self.repository = MedicoRepository()

    def criar_medico(self, nome: str) -> Medico:
        """Cria um novo médico com validação de dados"""
        if not nome or not nome.strip():
            raise ValueError("Nome do médico é obrigatório")
        
        nome = nome.strip()
        
        # Verifica se já existe um médico com o mesmo nome
        if self.repository.find_by_nome(nome):
            raise ValueError(f"Já existe um médico com o nome '{nome}'")
        
        return self.repository.create_medico(nome)

    def listar_medicos(self) -> List[Medico]:
        """Lista todos os médicos"""
        return self.repository.get_medicos()

    def buscar_medico(self, medico_id: int) -> Optional[Medico]:
        """Busca um médico por ID"""
        if medico_id <= 0:
            raise ValueError("ID do médico deve ser positivo")
        return self.repository.get_medico_by_id(medico_id)

    def atualizar_medico(self, medico_id: int, nome: str = None) -> Optional[Medico]:
        """Atualiza um médico com validação"""
        if medico_id <= 0:
            raise ValueError("ID do médico deve ser positivo")
        
        if nome is not None:
            nome = nome.strip()
            if not nome:
                raise ValueError("Nome não pode ser vazio")
            
            # Verifica se já existe outro médico com o mesmo nome
            medico_existente = self.repository.find_by_nome(nome)
            if medico_existente and medico_existente.id != medico_id:
                raise ValueError(f"Já existe um médico com o nome '{nome}'")
        
        return self.repository.update_medico(medico_id, nome)

    def excluir_medico(self, medico_id: int) -> bool:
        """Exclui um médico"""
        if medico_id <= 0:
            raise ValueError("ID do médico deve ser positivo")
        return self.repository.delete_medico(medico_id)

    def buscar_por_nome(self, nome: str) -> Optional[Medico]:
        """Busca médico por nome"""
        if not nome or not nome.strip():
            return None
        return self.repository.find_by_nome(nome.strip())

    def listar_medicos_por_especializacao(self, especializacao_id: int) -> List[Medico]:
        """Lista médicos por especialização"""
        if especializacao_id <= 0:
            raise ValueError("ID da especialização deve ser positivo")
        return self.repository.get_medicos_by_especializacao(especializacao_id)