from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.sobreaviso import Sobreaviso
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from app.models.database import SessionLocal
from sqlalchemy.orm import joinedload
from datetime import datetime

sobreaviso_bp = Blueprint("sobreavisos", __name__, url_prefix="/sobreavisos")


@sobreaviso_bp.route("/")
def list_sobreavisos():
    session_db = SessionLocal()
    sobreavisos = (
        session_db.query(Sobreaviso).options(joinedload(Sobreaviso.medico)).all()
    )
    doctors = session_db.query(Doctor).all()
    specializations = session_db.query(Specialization).all()
    session_db.close()
    return render_template(
        "sobreavisos/list.html",
        sobreavisos=sobreavisos,
        doctors=doctors,
        specializations=specializations,
    )


@sobreaviso_bp.route("/novo", methods=["GET", "POST"])
def create_sobreaviso():
    session_db = SessionLocal()
    doctors = session_db.query(Doctor).all()
    specializations = session_db.query(Specialization).all()
    if request.method == "POST":
        data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        especialidade = request.form["especialidade"]
        medico_id = request.form["medico_id"]
        sobreaviso = Sobreaviso(
            data=data,
            especialidade=especialidade,
            medico_id=medico_id,
        )
        session_db.add(sobreaviso)
        session_db.commit()
        flash("Escala de sobreaviso criada com sucesso!", "success")
        session_db.close()
        return redirect(url_for("sobreavisos.list_sobreavisos"))
    session_db.close()
    return render_template(
        "sobreavisos/form.html",
        doctors=doctors,
        specializations=specializations,
        sobreaviso=None,
    )


@sobreaviso_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def edit_sobreaviso(id):
    session_db = SessionLocal()
    sobreaviso = session_db.query(Sobreaviso).get(id)
    doctors = session_db.query(Doctor).all()
    specializations = session_db.query(Specialization).all()
    if not sobreaviso:
        flash("Escala não encontrada.", "danger")
        session_db.close()
        return redirect(url_for("sobreavisos.list_sobreavisos"))
    if request.method == "POST":
        sobreaviso.data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        sobreaviso.especialidade = request.form["especialidade"]
        sobreaviso.medico_id = request.form["medico_id"]
        session_db.commit()
        flash("Escala de sobreaviso atualizada com sucesso!", "success")
        session_db.close()
        return redirect(url_for("sobreavisos.list_sobreavisos"))
    session_db.close()
    return render_template(
        "sobreavisos/form.html",
        doctors=doctors,
        specializations=specializations,
        sobreaviso=sobreaviso,
    )


@sobreaviso_bp.route("/excluir/<int:id>", methods=["POST"])
def delete_sobreaviso(id):
    session_db = SessionLocal()
    sobreaviso = session_db.query(Sobreaviso).get(id)
    if not sobreaviso:
        flash("Escala não encontrada.", "danger")
    else:
        session_db.delete(sobreaviso)
        session_db.commit()
        flash("Escala de sobreaviso excluída com sucesso!", "success")
    session_db.close()
    return redirect(url_for("sobreavisos.list_sobreavisos"))
