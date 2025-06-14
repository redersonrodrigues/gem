from flask import Blueprint, render_template
from app.models.plantonista import Plantonista
from app.models.doctor import Doctor
from app.models.database import SessionLocal
from sqlalchemy.orm import joinedload

plantonista_bp = Blueprint("plantonistas", __name__, url_prefix="/plantonistas")


@plantonista_bp.route("/")
def list_plantonistas():
    session_db = SessionLocal()
    plantonistas = (
        session_db.query(Plantonista)
        .options(
            joinedload(Plantonista.diurno_medico1),
            joinedload(Plantonista.diurno_medico2),
            joinedload(Plantonista.noturno_medico1),
            joinedload(Plantonista.noturno_medico2),
        )
        .all()
    )
    doctors = session_db.query(Doctor).all()
    session_db.close()
    return render_template(
        "plantonistas/list.html", plantonistas=plantonistas, doctors=doctors
    )
