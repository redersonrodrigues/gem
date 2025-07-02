# Repositório para operações específicas de Hospital
from typing import List, Optional
from gem.models.base_models import Hospital
from .base_repository import BaseRepository


class HospitalRepository(BaseRepository):
    """Repositório para gerenciar operações de Hospital"""
    
    def __init__(self):
        super().__init__(Hospital)

    def create_hospital(self, nome: str, endereco: str) -> Hospital:
        """Cria um novo hospital"""
        return self.create(nome=nome, endereco=endereco)

    def get_hospitals(self) -> List[Hospital]:
        """Retorna todos os hospitais"""
        return self.get_all()

    def get_hospital_by_id(self, hospital_id: int) -> Optional[Hospital]:
        """Busca um hospital por ID"""
        return self.get_by_id(hospital_id)

    def update_hospital(self, hospital_id: int, nome: str = None, endereco: str = None) -> Optional[Hospital]:
        """Atualiza um hospital"""
        update_data = {}
        if nome is not None:
            update_data['nome'] = nome
        if endereco is not None:
            update_data['endereco'] = endereco
        return self.update(hospital_id, **update_data)

    def delete_hospital(self, hospital_id: int) -> bool:
        """Remove um hospital"""
        return self.delete(hospital_id)

    def find_by_nome(self, nome: str) -> List[Hospital]:
        """Busca hospitais por nome"""
        return self.filter_by(nome=nome)