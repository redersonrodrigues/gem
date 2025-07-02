# Serviço para gerenciamento de especializações
from typing import List, Optional
from gem.repositories.especializacao_repository import EspecializacaoRepository
from gem.models.base_models import Especializacao


class EspecializacaoService:
    """Serviço para lógica de negócio relacionada a especializações"""
    
    def __init__(self):
        self.repository = EspecializacaoRepository()

    def criar_especializacao(self, nome: str) -> Especializacao:
        """Cria uma nova especialização com validação de dados"""
        if not nome or not nome.strip():
            raise ValueError("Nome da especialização é obrigatório")
        
        nome = nome.strip()
        
        # Verifica se já existe uma especialização com o mesmo nome
        if self.repository.find_by_nome(nome):
            raise ValueError(f"Já existe uma especialização com o nome '{nome}'")
        
        return self.repository.create_especializacao(nome)

    def listar_especializacoes(self) -> List[Especializacao]:
        """Lista todas as especializações"""
        return self.repository.get_especializacoes()

    def buscar_especializacao(self, especializacao_id: int) -> Optional[Especializacao]:
        """Busca uma especialização por ID"""
        if especializacao_id <= 0:
            raise ValueError("ID da especialização deve ser positivo")
        return self.repository.get_especializacao_by_id(especializacao_id)

    def atualizar_especializacao(self, especializacao_id: int, nome: str = None) -> Optional[Especializacao]:
        """Atualiza uma especialização com validação"""
        if especializacao_id <= 0:
            raise ValueError("ID da especialização deve ser positivo")
        
        if nome is not None:
            nome = nome.strip()
            if not nome:
                raise ValueError("Nome não pode ser vazio")
            
            # Verifica se já existe outra especialização com o mesmo nome
            especializacao_existente = self.repository.find_by_nome(nome)
            if especializacao_existente and especializacao_existente.id != especializacao_id:
                raise ValueError(f"Já existe uma especialização com o nome '{nome}'")
        
        return self.repository.update_especializacao(especializacao_id, nome)

    def excluir_especializacao(self, especializacao_id: int) -> bool:
        """Exclui uma especialização"""
        if especializacao_id <= 0:
            raise ValueError("ID da especialização deve ser positivo")
        return self.repository.delete_especializacao(especializacao_id)

    def buscar_por_nome(self, nome: str) -> Optional[Especializacao]:
        """Busca especialização por nome"""
        if not nome or not nome.strip():
            return None
        return self.repository.find_by_nome(nome.strip())

    def listar_especializacoes_por_medico(self, medico_id: int) -> List[Especializacao]:
        """Lista especializações por médico"""
        if medico_id <= 0:
            raise ValueError("ID do médico deve ser positivo")
        return self.repository.get_especializacoes_by_medico(medico_id)

    def popular_especializacoes_iniciais(self) -> None:
        """Popula especializações iniciais no sistema"""
        especializacoes_iniciais = [
            "Cardiologia",
            "Ortopedia", 
            "Pediatria",
            "Neurologia",
            "Dermatologia"
        ]
        
        for nome in especializacoes_iniciais:
            if not self.repository.find_by_nome(nome):
                self.repository.create_especializacao(nome)