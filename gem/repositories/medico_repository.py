# Repositório para operações específicas de Médico
from typing import List, Optional
from gem.models.base_models import Medico
from .base_repository import BaseRepository


class MedicoRepository(BaseRepository):
    """Repositório para gerenciar operações de Médico"""
    
    def __init__(self):
        super().__init__(Medico)

    def create_medico(self, nome: str) -> Medico:
        """Cria um novo médico"""
        return self.create(nome=nome)

    def get_medicos(self) -> List[Medico]:
        """Retorna todos os médicos"""
        return self.get_all()

    def get_medico_by_id(self, medico_id: int) -> Optional[Medico]:
        """Busca um médico por ID"""
        return self.get_by_id(medico_id)

    def update_medico(self, medico_id: int, nome: str = None) -> Optional[Medico]:
        """Atualiza um médico"""
        update_data = {}
        if nome is not None:
            update_data['nome'] = nome.upper()  # Mantem a consistência do modelo
        return self.update(medico_id, **update_data)

    def delete_medico(self, medico_id: int) -> bool:
        """Remove um médico"""
        return self.delete(medico_id)

    def find_by_nome(self, nome: str) -> Optional[Medico]:
        """Busca médico por nome (nome é único)"""
        medicos = self.filter_by(nome=nome.upper())
        return medicos[0] if medicos else None

    def get_medicos_by_especializacao(self, especializacao_id: int) -> List[Medico]:
        """Retorna médicos por especialização"""
        return Medico.query.join(Medico.especializacoes).filter_by(id=especializacao_id).all()