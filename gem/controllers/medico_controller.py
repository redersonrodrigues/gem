# Controlador para gerenciamento de médicos
from typing import Dict, Any
from gem.services.medico_service import MedicoService
from .base_controller import BaseController


class MedicoController(BaseController):
    """Controlador para operações relacionadas a médicos"""
    
    def __init__(self):
        super().__init__()
        self.service = MedicoService()

    def criar_medico(self, nome: str) -> Dict[str, Any]:
        """Cria um novo médico"""
        try:
            medico = self.service.criar_medico(nome)
            return self.handle_success(
                data={
                    'id': medico.id,
                    'nome': medico.nome
                },
                message="Médico criado com sucesso"
            )
        except Exception as e:
            return self.handle_error(e)

    def listar_medicos(self) -> Dict[str, Any]:
        """Lista todos os médicos"""
        try:
            medicos = self.service.listar_medicos()
            data = [
                {
                    'id': m.id,
                    'nome': m.nome,
                    'especializacoes': [e.nome for e in m.especializacoes]
                }
                for m in medicos
            ]
            return self.handle_success(data=data)
        except Exception as e:
            return self.handle_error(e)

    def buscar_medico(self, medico_id: Any) -> Dict[str, Any]:
        """Busca um médico por ID"""
        try:
            id_validado = self.validate_id(medico_id)
            medico = self.service.buscar_medico(id_validado)
            
            if medico:
                data = {
                    'id': medico.id,
                    'nome': medico.nome,
                    'especializacoes': [e.nome for e in medico.especializacoes]
                }
                return self.handle_success(data=data)
            else:
                return self.handle_success(data=None, message="Médico não encontrado")
        except Exception as e:
            return self.handle_error(e)

    def atualizar_medico(self, medico_id: Any, nome: str = None) -> Dict[str, Any]:
        """Atualiza um médico"""
        try:
            id_validado = self.validate_id(medico_id)
            medico = self.service.atualizar_medico(id_validado, nome)
            
            if medico:
                data = {
                    'id': medico.id,
                    'nome': medico.nome,
                    'especializacoes': [e.nome for e in medico.especializacoes]
                }
                return self.handle_success(data=data, message="Médico atualizado com sucesso")
            else:
                return self.handle_success(data=None, message="Médico não encontrado")
        except Exception as e:
            return self.handle_error(e)

    def excluir_medico(self, medico_id: Any) -> Dict[str, Any]:
        """Exclui um médico"""
        try:
            id_validado = self.validate_id(medico_id)
            sucesso = self.service.excluir_medico(id_validado)
            
            if sucesso:
                return self.handle_success(message="Médico excluído com sucesso")
            else:
                return self.handle_success(message="Médico não encontrado")
        except Exception as e:
            return self.handle_error(e)

    def listar_medicos_por_especializacao(self, especializacao_id: Any) -> Dict[str, Any]:
        """Lista médicos por especialização"""
        try:
            id_validado = self.validate_id(especializacao_id)
            medicos = self.service.listar_medicos_por_especializacao(id_validado)
            data = [
                {
                    'id': m.id,
                    'nome': m.nome
                }
                for m in medicos
            ]
            return self.handle_success(data=data)
        except Exception as e:
            return self.handle_error(e)