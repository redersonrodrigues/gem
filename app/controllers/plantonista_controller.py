from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from sqlalchemy.sql import extract

from app.models.plantonista import Plantonista
from app.models.doctor import Doctor
from app.models.database import SessionLocal
from datetime import datetime
from app.models.plantonista_factory import PlantonistaFactory
from app.models.validation_strategy import ValidationStrategy
from app.models.notification_manager import NotificationManager

plantonista_bp = Blueprint("plantonistas", __name__,
                           url_prefix="/plantonistas")


@plantonista_bp.route("/")
def list_plantonistas():
    session_db = SessionLocal()
    mes = request.args.get("mes", default=None, type=int)
    query = session_db.query(Plantonista).options(
        joinedload(Plantonista.diurno_medico1),
        joinedload(Plantonista.diurno_medico2),
        joinedload(Plantonista.noturno_medico1),
        joinedload(Plantonista.noturno_medico2),
    )
    if mes:
        query = query.filter(extract("month", Plantonista.data) == mes)
    plantonistas = query.order_by(Plantonista.data.asc()).all()

    doctors = session_db.query(Doctor).all()
    doctors_dict = [{"id": d.id, "name": d.name} for d in doctors]
    session_db.close()
    return render_template("plantonistas/list.html", plantonistas=plantonistas, mes=mes)


@plantonista_bp.route("/novo", methods=["GET", "POST"])
def create_plantonista():
    session_db = SessionLocal()
    doctors = session_db.query(Doctor).all()
    if request.method == "POST":
        request_data = {
            "data": request.form.get("data"),
            "diurno_medico1_id": request.form.get("diurno_medico1_id"),
            "diurno_medico2_id": request.form.get("diurno_medico2_id"),
            "noturno_medico1_id": request.form.get("noturno_medico1_id"),
            "noturno_medico2_id": request.form.get("noturno_medico2_id"),
        }

        # Aplicar estratégia de validação
        validation_strategy = ValidationStrategy(session_db)
        validation_message = validation_strategy.validate(request_data)
        if validation_message:
            NotificationManager.error(validation_message)
            return render_template(
                "plantonistas/form.html",
                doctors=doctors,
                plantonista={
                    "data": request_data["data"],
                    "diurno_medico1_id": request_data["diurno_medico1_id"],
                    "diurno_medico2_id": request_data["diurno_medico2_id"],
                    "noturno_medico1_id": request_data["noturno_medico1_id"],
                    "noturno_medico2_id": request_data["noturno_medico2_id"],
                },
                is_edit=False
            )

        try:
            if isinstance(request_data["data"], str):
                request_data["data"] = datetime.strptime(
                    request_data["data"], "%Y-%m-%d").date()
        except ValueError as ve:
            NotificationManager.error("Erro de valor: " + str(ve))
            return render_template(
                "plantonistas/form.html",
                doctors=doctors,
                plantonista={
                    "data": request_data["data"],
                    "diurno_medico1_id": request_data["diurno_medico1_id"],
                    "diurno_medico2_id": request_data["diurno_medico2_id"],
                    "noturno_medico1_id": request_data["noturno_medico1_id"],
                    "noturno_medico2_id": request_data["noturno_medico2_id"],
                },
                is_edit=False
            )
        except Exception as e:
            NotificationManager.error("Erro inesperado: " + str(e))
            return render_template(
                "plantonistas/form.html",
                doctors=doctors,
                plantonista={
                    "data": request_data["data"],
                    "diurno_medico1_id": request_data["diurno_medico1_id"],
                    "diurno_medico2_id": request_data["diurno_medico2_id"],
                    "noturno_medico1_id": request_data["noturno_medico1_id"],
                    "noturno_medico2_id": request_data["noturno_medico2_id"],
                },
                is_edit=False
            )

        # Criar Plantonista usando Factory
        try:
            plantonista = PlantonistaFactory.create(request_data, session_db)
            session_db.add(plantonista)
            session_db.commit()
            NotificationManager.success("Plantonista cadastrado com sucesso!")
        except Exception as e:
            session_db.rollback()
            NotificationManager.error(f"Erro ao criar escala: {str(e)}")
        finally:
            session_db.close()
        return redirect(url_for("plantonistas.list_plantonistas"))

    session_db.close()
    return render_template("plantonistas/form.html", doctors=doctors, plantonista=None)


@plantonista_bp.route("/editar/<int:plantonista_id>", methods=["GET", "POST"])
def edit_plantonista(plantonista_id):
    session_db = SessionLocal()
    plantonista = session_db.query(Plantonista).get(plantonista_id)
    doctors = session_db.query(Doctor).all()
    if not plantonista:
        flash("Escala não encontrada.", "danger")
        session_db.close()
        return redirect(url_for("plantonistas.list_plantonistas"))

    if request.method == "POST":
        request_data = {
            "data": request.form.get("data"),
            "diurno_medico1_id": request.form.get("diurno_medico1_id"),
            "diurno_medico2_id": request.form.get("diurno_medico2_id"),
            "noturno_medico1_id": request.form.get("noturno_medico1_id"),
            "noturno_medico2_id": request.form.get("noturno_medico2_id"),
        }

        # Ajusta para verificar valores reais, incluindo None e strings vazias
        for key, value in request_data.items():
            if value is None or str(value).strip() == "":
                flash(f"O campo {key} é obrigatório.", "danger")
                return render_template("plantonistas/form.html", doctors=doctors, plantonista=plantonista)

        # Validação: não permitir médicos com nomes iguais no mesmo turno
        diurno_medicos = [
            session_db.query(Doctor).get(
                request_data["diurno_medico1_id"]).name,
            session_db.query(Doctor).get(
                request_data["diurno_medico2_id"]).name,
        ]
        noturno_medicos = [
            session_db.query(Doctor).get(
                request_data["noturno_medico1_id"]).name,
            session_db.query(Doctor).get(
                request_data["noturno_medico2_id"]).name,
        ]
        if len(set(diurno_medicos)) < len(diurno_medicos):
            flash("Médicos no turno diurno devem ter nomes diferentes.", "danger")
            return render_template(
                "plantonistas/form.html",
                doctors=doctors,
                plantonista=request_data
            )
        if len(set(noturno_medicos)) < len(noturno_medicos):
            flash("Médicos no turno noturno devem ter nomes diferentes.", "danger")
            return render_template(
                "plantonistas/form.html",
                doctors=doctors,
                plantonista=request_data
            )

        try:
            plantonista.data = datetime.strptime(
                request_data["data"], "%Y-%m-%d").date()
            plantonista.diurno_medico1_id = request_data["diurno_medico1_id"]
            plantonista.diurno_medico2_id = request_data["diurno_medico2_id"]
            plantonista.noturno_medico1_id = request_data["noturno_medico1_id"]
            plantonista.noturno_medico2_id = request_data["noturno_medico2_id"]

            session_db.commit()
            flash("Escala de plantonista atualizada com sucesso!", "success")
        except Exception as e:
            session_db.rollback()
            flash(f"Erro ao atualizar escala: {str(e)}", "danger")
        finally:
            session_db.close()
            return redirect(url_for("plantonistas.list_plantonistas"))

    session_db.close()
    return render_template("plantonistas/form.html", doctors=doctors, plantonista=plantonista)


@plantonista_bp.route("/excluir/<int:plantonista_id>", methods=["POST"])
def delete_plantonista(plantonista_id):
    session_db = SessionLocal()
    plantonista = session_db.query(Plantonista).get(plantonista_id)
    if not plantonista:
        flash("Escala não encontrada.", "danger")
    else:
        session_db.delete(plantonista)
        session_db.commit()
        flash("Escala de plantonista excluída com sucesso!", "success")
    session_db.close()
    return redirect(url_for("plantonistas.list_plantonistas"))


class Handler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return None


class RequiredFieldHandler(Handler):
    def handle(self, request):
        if not request.get("field"):
            return "Campo obrigatório está vazio."
        return super().handle(request)


class UniqueFieldHandler(Handler):
    def handle(self, request):
        if request.get("field") in ["valor_existente"]:
            return "Valor já existe."
        return super().handle(request)


class ValidationHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return None


class RequiredFieldValidation(ValidationHandler):
    def __init__(self, field, message, next_handler=None):
        super().__init__(next_handler)
        self.field = field
        self.message = message

    def handle(self, request):
        # Ajusta para verificar valores reais, incluindo None e strings vazias
        value = request.get(self.field)
        if value is None or str(value).strip() == "":
            return self.message
        return super().handle(request)


class UniqueFieldValidation(ValidationHandler):
    def __init__(self, field, existing_values, message, next_handler=None):
        super().__init__(next_handler)
        self.field = field
        self.existing_values = existing_values
        self.message = message

    def handle(self, request):
        if request.get(self.field) in self.existing_values:
            return self.message
        return super().handle(request)
