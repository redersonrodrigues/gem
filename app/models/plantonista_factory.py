from app.models.plantonista import Plantonista
from datetime import datetime


class PlantonistaFactory:
    @staticmethod
    def create(data, session):
        try:
            # Converter data para datetime.date
            if isinstance(data["data"], str):
                data["data"] = datetime.strptime(
                    data["data"], "%Y-%m-%d").date()

            # Criar instância de Plantonista
            plantonista = Plantonista(
                data=data["data"],
                diurno_medico1_id=data["diurno_medico1_id"],
                diurno_medico2_id=data["diurno_medico2_id"],
                noturno_medico1_id=data["noturno_medico1_id"],
                noturno_medico2_id=data["noturno_medico2_id"],
            )
            return plantonista
        except Exception as e:
            raise ValueError(f"Erro ao criar Plantonista: {str(e)}")
