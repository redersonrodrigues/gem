# Repositório para operações específicas de Especialização
from typing import List, Optional
from gem.models.base_models import Especializacao
from .base_repository import BaseRepository


class EspecializacaoRepository(BaseRepository):
    """Repositório para gerenciar operações de Especialização"""
    
    def __init__(self):
        super().__init__(Especializacao)

    def create_especializacao(self, nome: str) -> Especializacao:
        """Cria uma nova especialização"""
        return self.create(nome=nome)

    def get_especializacoes(self) -> List[Especializacao]:
        """Retorna todas as especializações"""
        return self.get_all()

    def get_especializacao_by_id(self, especializacao_id: int) -> Optional[Especializacao]:
        """Busca uma especialização por ID"""
        return self.get_by_id(especializacao_id)

    def update_especializacao(self, especializacao_id: int, nome: str = None) -> Optional[Especializacao]:
        """Atualiza uma especialização"""
        update_data = {}
        if nome is not None:
            update_data['nome'] = nome.upper()  # Mantem a consistência do modelo
        return self.update(especializacao_id, **update_data)

    def delete_especializacao(self, especializacao_id: int) -> bool:
        """Remove uma especialização"""
        return self.delete(especializacao_id)

    def find_by_nome(self, nome: str) -> Optional[Especializacao]:
        """Busca especialização por nome (nome é único)"""
        especializacoes = self.filter_by(nome=nome.upper())
        return especializacoes[0] if especializacoes else None

    def get_especializacoes_by_medico(self, medico_id: int) -> List[Especializacao]:
        """Retorna especializações por médico"""
        return Especializacao.query.join(Especializacao.medicos).filter_by(id=medico_id).all()