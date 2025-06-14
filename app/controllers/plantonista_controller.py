from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.plantonista import Plantonista
from app.models.doctor import Doctor
from app.models.database import SessionLocal
from sqlalchemy.orm import joinedload
from datetime import datetime

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


@plantonista_bp.route("/novo", methods=["GET", "POST"])
def create_plantonista():
    session_db = SessionLocal()
    doctors = session_db.query(Doctor).all()
    if request.method == "POST":
        data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        diurno_medico1_id = request.form["diurno_medico1_id"]
        diurno_medico2_id = request.form["diurno_medico2_id"]
        noturno_medico1_id = request.form["noturno_medico1_id"]
        noturno_medico2_id = request.form["noturno_medico2_id"]
        plantonista = Plantonista(
            data=data,
            diurno_medico1_id=diurno_medico1_id,
            diurno_medico2_id=diurno_medico2_id,
            noturno_medico1_id=noturno_medico1_id,
            noturno_medico2_id=noturno_medico2_id,
        )
        session_db.add(plantonista)
        session_db.commit()
        flash("Escala de plantonista criada com sucesso!", "success")
        session_db.close()
        return redirect(url_for("plantonistas.list_plantonistas"))
    session_db.close()
    return render_template("plantonistas/form.html", doctors=doctors, plantonista=None)


@plantonista_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def edit_plantonista(id):
    session_db = SessionLocal()
    plantonista = session_db.query(Plantonista).get(id)
    doctors = session_db.query(Doctor).all()
    if not plantonista:
        flash("Escala não encontrada.", "danger")
        session_db.close()
        return redirect(url_for("plantonistas.list_plantonistas"))
    if request.method == "POST":
        plantonista.data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        plantonista.diurno_medico1_id = request.form["diurno_medico1_id"]
        plantonista.diurno_medico2_id = request.form["diurno_medico2_id"]
        plantonista.noturno_medico1_id = request.form["noturno_medico1_id"]
        plantonista.noturno_medico2_id = request.form["noturno_medico2_id"]
        session_db.commit()
        flash("Escala de plantonista atualizada com sucesso!", "success")
        session_db.close()
        return redirect(url_for("plantonistas.list_plantonistas"))
    session_db.close()
    return render_template(
        "plantonistas/form.html", doctors=doctors, plantonista=plantonista
    )


@plantonista_bp.route("/excluir/<int:id>", methods=["POST"])
def delete_plantonista(id):
    session_db = SessionLocal()
    plantonista = session_db.query(Plantonista).get(id)
    if not plantonista:
        flash("Escala não encontrada.", "danger")
    else:
        session_db.delete(plantonista)
        session_db.commit()
        flash("Escala de plantonista excluída com sucesso!", "success")
    session_db.close()
    return redirect(url_for("plantonistas.list_plantonistas"))
