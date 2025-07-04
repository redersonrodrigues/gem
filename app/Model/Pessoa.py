class Pessoa:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @staticmethod
    def all():
        # Simula dados vindos do banco
        return [
            Pessoa(1, "Maria"),
            Pessoa(2, "José"),
            Pessoa(3, "Ana")
        ]