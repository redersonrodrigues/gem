# Controladores da aplicação

from .base_controller import BaseController
from .hospital_controller import HospitalController
from .medico_controller import MedicoController

__all__ = [
    'BaseController',
    'HospitalController',
    'MedicoController'
]