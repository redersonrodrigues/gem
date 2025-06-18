from app.models.plantonista import Plantonista
from app.models.doctor import Doctor
from app.models.notification_manager import NotificationManager


class ValidationStrategy:
    def __init__(self, session):
        self.session = session

    def validate(self, data):
        # Validação: não permitir registro na mesma data
        if self.session.query(Plantonista).filter_by(data=data["data"]).first():
            NotificationManager.error(
                "Já existe uma escala registrada para esta data.")
            return False

        # Validação: não permitir médicos com nomes iguais no mesmo turno
        diurno_medicos = [
            self.session.query(Doctor).get(data["diurno_medico1_id"]).name,
            self.session.query(Doctor).get(data["diurno_medico2_id"]).name,
        ]
        noturno_medicos = [
            self.session.query(Doctor).get(data["noturno_medico1_id"]).name,
            self.session.query(Doctor).get(data["noturno_medico2_id"]).name,
        ]
        if len(set(diurno_medicos)) < len(diurno_medicos):
            NotificationManager.error(
                "Médicos no turno diurno devem ter nomes diferentes.")
            return False
        if len(set(noturno_medicos)) < len(noturno_medicos):
            NotificationManager.error(
                "Médicos no turno noturno devem ter nomes diferentes.")
            return False

        NotificationManager.success("Validação concluída com sucesso.")
        return True
