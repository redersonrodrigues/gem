from app.Strategy.escala_factory import EscalaFactory

class GerenciadorEscalas:
    def __init__(self, tipo_escala):
        self._strategy = EscalaFactory.get_strategy(tipo_escala)

    def set_tipo_escala(self, tipo_escala):
        self._strategy = EscalaFactory.get_strategy(tipo_escala)

    def criar_escala(self, **kwargs):
        return self._strategy.criar_escala(**kwargs)

    def buscar_escala(self, **kwargs):
        return self._strategy.buscar_escala(**kwargs)
