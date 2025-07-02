# Modelos de dados da aplicação

from .base_models import (
    Hospital, Medico, Especializacao, User, Log,
    medico_especializacao
)
from .escala_models import (
    Escala, EscalaPlantonista, EscalaSobreaviso,
    EscalaStrategy, EscalaPlantonista as EscalaPlantonistStrategy,
    EscalaSobreaviso as EscalaSobreavisoStrategy,
    Base
)

__all__ = [
    'Hospital', 'Medico', 'Especializacao', 'User', 'Log',
    'Escala', 'EscalaPlantonista', 'EscalaSobreaviso',
    'EscalaStrategy', 'EscalaPlantonistStrategy', 'EscalaSobreavisoStrategy',
    'medico_especializacao', 'Base'
]