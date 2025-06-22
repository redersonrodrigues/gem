"""
Módulo utilitário para validação de dados de entrada.
Inclui funções para validar campos obrigatórios, tipos, formatos e restrições de negócio.
"""
from typing import Any, Dict, List, Type
from datetime import datetime
import re

class ValidationError(Exception):
    pass

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]):
    missing = [field for field in required_fields if field not in data or data[field] in (None, "")]
    if missing:
        raise ValidationError(f"Campos obrigatórios ausentes: {', '.join(missing)}")

def validate_date_format(date_str: str, fmt: str = "%Y-%m-%d"):
    try:
        datetime.strptime(date_str, fmt)
    except Exception:
        raise ValidationError(f"Data inválida: {date_str}. Formato esperado: {fmt}")

def validate_email(email: str):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise ValidationError(f"E-mail inválido: {email}")

def validate_positive_int(value: Any, field: str):
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(f"O campo '{field}' deve ser um inteiro positivo.")

def validate_foreign_key_exists(session, model: Type, key_value: Any, key_field: str = 'id'):
    """
    Valida se o registro relacionado existe na tabela de destino.
    Exemplo: validate_foreign_key_exists(db.session, Medico, medico_id)
    """
    exists = session.query(model).filter(getattr(model, key_field) == key_value).first()
    if not exists:
        raise ValidationError(f"Registro relacionado não encontrado: {model.__name__}({key_field}={key_value})")

# Outras funções de validação podem ser adicionadas conforme a necessidade do domínio.
