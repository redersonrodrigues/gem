"""
Utilitários para controle de permissões baseado em perfil de usuário.
"""
from datetime import date

ADMIN_ROLE = 'admin'
USER_ROLE = 'usuario'


def is_admin(user):
    """Retorna True se o usuário for admin."""
    return getattr(user, 'perfil', None) == ADMIN_ROLE


def can_edit(user, data_referencia: date) -> bool:
    """
    Usuário admin pode editar sempre.
    Usuário comum só pode editar até o dia 15 do mês seguinte à data de referência.
    """
    if is_admin(user):
        return True
    hoje = date.today()
    limite = date(data_referencia.year, data_referencia.month, 1)
    # Avança para o mês seguinte
    if limite.month == 12:
        limite = date(limite.year + 1, 1, 1)
    else:
        limite = date(limite.year, limite.month + 1, 1)
    limite = limite.replace(day=15)
    return hoje <= limite
