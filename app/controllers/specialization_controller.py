from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.database import SessionLocal
from app.models.specialization import Specialization

specialization_bp = Blueprint(
    "specializations", __name__, url_prefix="/specializations"
)


@specialization_bp.route("/", methods=["GET", "POST"])
def manage_specializations():
    session_db = SessionLocal()
    if request.method == "POST":
        name = request.form.get("name", "").strip().upper()
        if name:
            if session_db.query(Specialization).filter_by(name=name).first():
                flash("Já existe uma especialização com esse nome.", "danger")
            else:
                specialization = Specialization(name=name)
                session_db.add(specialization)
                session_db.commit()
                flash("Especialização cadastrada com sucesso!", "success")
        else:
            flash("O nome da especialização não pode estar vazio.", "danger")
        return redirect(url_for("specializations.manage_specializations"))

    specializations = session_db.query(Specialization).all()
    session_db.close()
    return render_template(
        "specialization_form.html", specializations=specializations
    )


@specialization_bp.route("/edit/<int:spec_id>", methods=["GET", "POST"])
def edit_specialization(spec_id):
    session_db = SessionLocal()
    specialization = session_db.query(Specialization).get(spec_id)
    if not specialization:
        flash("Especialização não encontrada.", "danger")
        session_db.close()
        return redirect(url_for("specializations.manage_specializations"))

    if request.method == "POST":
        name = request.form.get("name", "").strip().upper()
        if name:
            if session_db.query(Specialization).filter(
                Specialization.name == name, Specialization.id != spec_id
            ).first():
                flash("Já existe uma especialização com esse nome.", "danger")
            else:
                specialization.name = name
                session_db.commit()
                flash("Especialização atualizada com sucesso!", "success")
                return redirect(
                    url_for("specializations.manage_specializations")
                )
        else:
            flash("O nome da especialização não pode estar vazio.", "danger")

    session_db.close()
    return render_template(
        "specialization_form.html", edit_specialization=specialization
    )


@specialization_bp.route("/delete/<int:spec_id>", methods=["POST"])
def delete_specialization(spec_id):
    session_db = SessionLocal()
    specialization = session_db.query(Specialization).get(spec_id)
    if specialization:
        session_db.delete(specialization)
        session_db.commit()
        flash("Especialização removida com sucesso!", "success")
    else:
        flash("Especialização não encontrada.", "danger")

    session_db.close()
    return redirect(url_for("specializations.manage_specializations"))
