"""
Validação de formulários e feedback visual para PyQt5
"""
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPalette, QColor

class FormValidator:
    @staticmethod
    def validate_required(field: QLineEdit, message: str = "Campo obrigatório") -> bool:
        if not field.text().strip():
            FormValidator.set_error(field, message)
            return False
        FormValidator.clear_error(field)
        return True

    @staticmethod
    def set_error(field: QLineEdit, message: str):
        palette = field.palette()
        palette.setColor(QPalette.Base, QColor('#ffe6e6'))
        field.setPalette(palette)
        field.setToolTip(message)

    @staticmethod
    def clear_error(field: QLineEdit):
        palette = field.palette()
        palette.setColor(QPalette.Base, QColor('white'))
        field.setPalette(palette)
        field.setToolTip("")

    @staticmethod
    def validate_email(
        field: QLineEdit,
        message: str = "E-mail inválido"
    ) -> bool:
        import re
        value = field.text().strip()
        if not value or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            FormValidator.set_error(field, message)
            return False
        FormValidator.clear_error(field)
        return True

    @staticmethod
    def validate_cpf(
        field: QLineEdit,
        message: str = "CPF inválido"
    ) -> bool:
        value = field.text().strip()
        if not value or not FormValidator._is_valid_cpf(value):
            FormValidator.set_error(field, message)
            return False
        FormValidator.clear_error(field)
        return True

    @staticmethod
    def _is_valid_cpf(cpf: str) -> bool:
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
            check = ((value * 10) % 11) % 10
            if check != int(cpf[i]):
                return False
        return True

    @staticmethod
    def validate_number(
        field: QLineEdit,
        message: str = "Valor numérico inválido"
    ) -> bool:
        value = field.text().strip()
        try:
            float(value)
            FormValidator.clear_error(field)
            return True
        except ValueError:
            FormValidator.set_error(field, message)
            return False

    @staticmethod
    def validate_min_length(
        field: QLineEdit,
        min_length: int,
        message: str = None
    ) -> bool:
        value = field.text().strip()
        if len(value) < min_length:
            msg = message or f"Mínimo de {min_length} caracteres"
            FormValidator.set_error(field, msg)
            return False
        FormValidator.clear_error(field)
        return True

    @staticmethod
    def validate_max_length(
        field: QLineEdit,
        max_length: int,
        message: str = None
    ) -> bool:
        value = field.text().strip()
        if len(value) > max_length:
            msg = message or f"Máximo de {max_length} caracteres"
            FormValidator.set_error(field, msg)
            return False
        FormValidator.clear_error(field)
        return True

    @staticmethod
    def validate_regex(
        field: QLineEdit,
        pattern: str,
        message: str = "Formato inválido"
    ) -> bool:
        import re
        value = field.text().strip()
        if not re.match(pattern, value):
            FormValidator.set_error(field, message)
            return False
        FormValidator.clear_error(field)
        return True

    @staticmethod
    def validate_date(
        field: QLineEdit,
        message: str = "Data inválida (formato DD/MM/AAAA)"
    ) -> bool:
        import datetime
        value = field.text().strip()
        try:
            datetime.datetime.strptime(value, "%d/%m/%Y")
            FormValidator.clear_error(field)
            return True
        except ValueError:
            FormValidator.set_error(field, message)
            return False

    @staticmethod
    def validate_custom(
        field,
        validator_func,
        message: str = "Valor inválido"
    ) -> bool:
        if not validator_func(field.text().strip()):
            FormValidator.set_error(field, message)
            return False
        FormValidator.clear_error(field)
        return True

    @staticmethod
    def validate_combobox_required(
        combobox,
        message: str = "Seleção obrigatória"
    ) -> bool:
        if combobox.currentIndex() == -1 or not combobox.currentText().strip():
            combobox.setStyleSheet("background-color: #ffe6e6;")
            combobox.setToolTip(message)
            return False
        combobox.setStyleSheet("")
        combobox.setToolTip("")
        return True

    @staticmethod
    def validate_all(validations: list) -> bool:
        """
        Recebe uma lista de funções de validação e retorna True se todas forem True.
        """
        return all(validations)
