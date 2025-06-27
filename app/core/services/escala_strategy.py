from abc import ABC, abstractmethod

class EscalaStrategy(ABC):
    @abstractmethod
    def validar(self, escala):
        pass

    @abstractmethod
    def salvar(self, escala):
        pass

class PlantonistaStrategy(EscalaStrategy):
    def validar(self, escala):
        # Exemplo de validação: checar campos obrigatórios
        required_fields = ['data', 'medico_id', 'turno']
        for field in required_fields:
            if field not in escala or not escala[field]:
                raise ValueError(f"Campo obrigatório ausente ou vazio: {field}")
        # Exemplo de regra: turno deve ser 'dia' ou 'noite'
        if escala['turno'] not in ['dia', 'noite']:
            raise ValueError("Turno inválido para plantonista. Use 'dia' ou 'noite'.")
        return True

    def salvar(self, escala):
        # Simulação de salvamento (poderia ser integração com DB)
        print(f"Salvando escala de plantonista: {escala}")
        return True

class SobreavisoStrategy(EscalaStrategy):
    def validar(self, escala):
        # Exemplo de validação: checar campos obrigatórios
        required_fields = ['data', 'medico_id', 'periodo']
        for field in required_fields:
            if field not in escala or not escala[field]:
                raise ValueError(f"Campo obrigatório ausente ou vazio: {field}")
        # Exemplo de regra: periodo deve ser 'manha', 'tarde' ou 'noite'
        if escala['periodo'] not in ['manha', 'tarde', 'noite']:
            raise ValueError("Período inválido para sobreaviso. Use 'manha', 'tarde' ou 'noite'.")
        return True

    def salvar(self, escala):
        # Simulação de salvamento (poderia ser integração com DB)
        print(f"Salvando escala de sobreaviso: {escala}")
        return True
