# Repositórios de dados da aplicação

from .base_repository import BaseRepository
from .hospital_repository import HospitalRepository
from .medico_repository import MedicoRepository
from .especializacao_repository import EspecializacaoRepository

__all__ = [
    'BaseRepository',
    'HospitalRepository', 
    'MedicoRepository',
    'EspecializacaoRepository'
]