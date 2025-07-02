# Serviço para gerenciamento de hospitais
from typing import List, Optional
from gem.repositories.hospital_repository import HospitalRepository
from gem.models.base_models import Hospital


class HospitalService:
    """Serviço para lógica de negócio relacionada a hospitais"""
    
    def __init__(self):
        self.repository = HospitalRepository()

    def criar_hospital(self, nome: str, endereco: str) -> Hospital:
        """Cria um novo hospital com validação de dados"""
        if not nome or not nome.strip():
            raise ValueError("Nome do hospital é obrigatório")
        if not endereco or not endereco.strip():
            raise ValueError("Endereço do hospital é obrigatório")
        
        nome = nome.strip()
        endereco = endereco.strip()
        
        return self.repository.create_hospital(nome, endereco)

    def listar_hospitais(self) -> List[Hospital]:
        """Lista todos os hospitais"""
        return self.repository.get_hospitals()

    def buscar_hospital(self, hospital_id: int) -> Optional[Hospital]:
        """Busca um hospital por ID"""
        if hospital_id <= 0:
            raise ValueError("ID do hospital deve ser positivo")
        return self.repository.get_hospital_by_id(hospital_id)

    def atualizar_hospital(self, hospital_id: int, nome: str = None, endereco: str = None) -> Optional[Hospital]:
        """Atualiza um hospital com validação"""
        if hospital_id <= 0:
            raise ValueError("ID do hospital deve ser positivo")
        
        if nome is not None:
            nome = nome.strip()
            if not nome:
                raise ValueError("Nome não pode ser vazio")
        
        if endereco is not None:
            endereco = endereco.strip()
            if not endereco:
                raise ValueError("Endereço não pode ser vazio")
        
        return self.repository.update_hospital(hospital_id, nome, endereco)

    def excluir_hospital(self, hospital_id: int) -> bool:
        """Exclui um hospital"""
        if hospital_id <= 0:
            raise ValueError("ID do hospital deve ser positivo")
        return self.repository.delete_hospital(hospital_id)

    def buscar_por_nome(self, nome: str) -> List[Hospital]:
        """Busca hospitais por nome"""
        if not nome or not nome.strip():
            return []
        return self.repository.find_by_nome(nome.strip())