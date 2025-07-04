from app.Strategy.escala_strategy import EscalaPlantonistaStrategy, EscalaSobreavisoStrategy

class EscalaFactory:
    @staticmethod
    def get_strategy(tipo_escala):
        if tipo_escala == "plantonista":
            return EscalaPlantonistaStrategy()
        elif tipo_escala == "sobreaviso":
            return EscalaSobreavisoStrategy()
        else:
            raise ValueError("Tipo de escala desconhecido")
