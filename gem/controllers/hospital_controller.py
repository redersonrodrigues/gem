# Controlador para gerenciamento de hospitais
from typing import Dict, Any
from gem.services.hospital_service import HospitalService
from .base_controller import BaseController


class HospitalController(BaseController):
    """Controlador para operações relacionadas a hospitais"""
    
    def __init__(self):
        super().__init__()
        self.service = HospitalService()

    def criar_hospital(self, nome: str, endereco: str) -> Dict[str, Any]:
        """Cria um novo hospital"""
        try:
            hospital = self.service.criar_hospital(nome, endereco)
            return self.handle_success(
                data={
                    'id': hospital.id,
                    'nome': hospital.nome,
                    'endereco': hospital.endereco
                },
                message="Hospital criado com sucesso"
            )
        except Exception as e:
            return self.handle_error(e)

    def listar_hospitais(self) -> Dict[str, Any]:
        """Lista todos os hospitais"""
        try:
            hospitais = self.service.listar_hospitais()
            data = [
                {
                    'id': h.id,
                    'nome': h.nome,
                    'endereco': h.endereco
                }
                for h in hospitais
            ]
            return self.handle_success(data=data)
        except Exception as e:
            return self.handle_error(e)

    def buscar_hospital(self, hospital_id: Any) -> Dict[str, Any]:
        """Busca um hospital por ID"""
        try:
            id_validado = self.validate_id(hospital_id)
            hospital = self.service.buscar_hospital(id_validado)
            
            if hospital:
                data = {
                    'id': hospital.id,
                    'nome': hospital.nome,
                    'endereco': hospital.endereco
                }
                return self.handle_success(data=data)
            else:
                return self.handle_success(data=None, message="Hospital não encontrado")
        except Exception as e:
            return self.handle_error(e)

    def atualizar_hospital(self, hospital_id: Any, nome: str = None, endereco: str = None) -> Dict[str, Any]:
        """Atualiza um hospital"""
        try:
            id_validado = self.validate_id(hospital_id)
            hospital = self.service.atualizar_hospital(id_validado, nome, endereco)
            
            if hospital:
                data = {
                    'id': hospital.id,
                    'nome': hospital.nome,
                    'endereco': hospital.endereco
                }
                return self.handle_success(data=data, message="Hospital atualizado com sucesso")
            else:
                return self.handle_success(data=None, message="Hospital não encontrado")
        except Exception as e:
            return self.handle_error(e)

    def excluir_hospital(self, hospital_id: Any) -> Dict[str, Any]:
        """Exclui um hospital"""
        try:
            id_validado = self.validate_id(hospital_id)
            sucesso = self.service.excluir_hospital(id_validado)
            
            if sucesso:
                return self.handle_success(message="Hospital excluído com sucesso")
            else:
                return self.handle_success(message="Hospital não encontrado")
        except Exception as e:
            return self.handle_error(e)