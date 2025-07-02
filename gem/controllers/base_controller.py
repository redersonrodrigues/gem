# Controlador base para operações comuns
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseController(ABC):
    """Classe base para controladores"""
    
    def __init__(self):
        self.service = None

    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Trata erros e retorna resposta padronizada"""
        return {
            'success': False,
            'error': str(error),
            'data': None
        }

    def handle_success(self, data: Any = None, message: str = None) -> Dict[str, Any]:
        """Trata sucesso e retorna resposta padronizada"""
        return {
            'success': True,
            'error': None,
            'data': data,
            'message': message
        }

    def validate_id(self, id_value: Any) -> int:
        """Valida se o ID é um número inteiro positivo"""
        try:
            id_int = int(id_value)
            if id_int <= 0:
                raise ValueError("ID deve ser um número positivo")
            return id_int
        except (ValueError, TypeError):
            raise ValueError("ID deve ser um número válido")