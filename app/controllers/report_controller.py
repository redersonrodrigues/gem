from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.report import Report
from app.models.database import SessionLocal
from app.models.plantonista import Plantonista
from app.models.sobreaviso import Sobreaviso
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import datetime
from collections import OrderedDict

report_bp = Blueprint("reports", __name__, url_prefix="/reports")


@report_bp.route("/novo", methods=["GET", "POST"])
def create_report():
    session_db = SessionLocal()
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        type = request.form["type"]
        filters = request.form["filters"]
        report = Report(name=name, description=description,
                        type=type, filters=filters)
        session_db.add(report)
        session_db.commit()
        flash("Relatório criado com sucesso!", "success")
        session_db.close()
        return redirect(url_for("reports.list_reports"))
    session_db.close()
    return render_template("reports/form.html", report=None)


@report_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def edit_report(id):
    session_db = SessionLocal()
    report = session_db.query(Report).get(id)
    if not report:
        flash("Relatório não encontrado.", "danger")
        session_db.close()
        return redirect(url_for("reports.list_reports"))
    if request.method == "POST":
        report.name = request.form["name"]
        report.description = request.form["description"]
        report.type = request.form["type"]
        report.filters = request.form["filters"]
        session_db.commit()
        flash("Relatório atualizado com sucesso!", "success")
        session_db.close()
        return redirect(url_for("reports.list_reports"))
    session_db.close()
    return render_template("reports/form.html", report=report)


@report_bp.route("/excluir/<int:id>", methods=["POST"])
def delete_report(id):
    session_db = SessionLocal()
    report = session_db.query(Report).get(id)
    if not report:
        flash("Relatório não encontrado.", "danger")
    else:
        session_db.delete(report)
        session_db.commit()
        flash("Relatório excluído com sucesso!", "success")
    session_db.close()
    return redirect(url_for("reports.list_reports"))


@report_bp.route("/plantonistas", methods=["GET"])
def report_plantonistas():
    session_db = SessionLocal()
    mes = request.args.get("mes", default=datetime.now().month, type=int)
    ano = request.args.get("ano", default=datetime.now().year, type=int)
    plantonistas = (
        session_db.query(Plantonista)
        .options(
            joinedload(Plantonista.diurno_medico1),
            joinedload(Plantonista.diurno_medico2),
            joinedload(Plantonista.noturno_medico1),
            joinedload(Plantonista.noturno_medico2),
        )
        .filter(
            func.extract("month", Plantonista.data) == mes,
            func.extract("year", Plantonista.data) == ano,
        )
        .order_by(Plantonista.data)
        .all()
    )
    session_db.close()
    return render_template(
        "reports/plantonistas.html", plantonistas=plantonistas, mes=mes, ano=ano
    )


@report_bp.route("/sobreavisos", methods=["GET"])
def report_sobreavisos():
    session_db = SessionLocal()
    mes = request.args.get("mes", default=datetime.now().month, type=int)
    ano = request.args.get("ano", default=datetime.now().year, type=int)
    sobreavisos = (
        session_db.query(Sobreaviso)
        .options(joinedload(Sobreaviso.medico))
        .filter(
            func.extract("month", Sobreaviso.data) == mes,
            func.extract("year", Sobreaviso.data) == ano,
        )
        .order_by(Sobreaviso.data)
        .all()
    )
    session_db.close()
    return render_template(
        "reports/sobreavisos.html", sobreavisos=sobreavisos, mes=mes, ano=ano
    )


@report_bp.route("/doctors", methods=["GET"])
def report_doctors():
    session_db = SessionLocal()
    especialidade_id = request.args.get("especialidade_id", type=int)
    busca_nome = request.args.get("busca_nome", default="", type=str).strip()

    especialidades = (
        session_db.query(Specialization).order_by(Specialization.name).all()
    )
    medicos_por_especialidade = {}

    for esp in especialidades:
        if especialidade_id and esp.id != especialidade_id:
            continue
        query = (
            session_db.query(Doctor)
            .join(Doctor.specializations)
            .filter(Specialization.id == esp.id)
        )
        if busca_nome:
            query = query.filter(Doctor.name.ilike(f"%{busca_nome}%"))
        medicos = query.order_by(Doctor.name).all()
        if medicos:
            medicos_por_especialidade[esp.name] = medicos

    session_db.close()
    return render_template(
        "reports/doctors.html",
        medicos_por_especialidade=medicos_por_especialidade,
        especialidades=especialidades,
        especialidade_id=especialidade_id,
        busca_nome=busca_nome,
    )


@report_bp.route("/imprimir", methods=["GET"])
def imprimir_relatorio():
    session_db = SessionLocal()
    mes = request.args.get("mes", default=datetime.now().month, type=int)
    ano = request.args.get("ano", default=datetime.now().year, type=int)
    plantonistas = (
        session_db.query(Plantonista)
        .options(
            joinedload(Plantonista.diurno_medico1),
            joinedload(Plantonista.diurno_medico2),
            joinedload(Plantonista.noturno_medico1),
            joinedload(Plantonista.noturno_medico2),
        )
        .filter(
            func.extract("month", Plantonista.data) == mes,
            func.extract("year", Plantonista.data) == ano,
        )
        .order_by(Plantonista.data)
        .all()
    )
    sobreavisos = (
        session_db.query(Sobreaviso)
        .options(joinedload(Sobreaviso.medico))
        .filter(
            func.extract("month", Sobreaviso.data) == mes,
            func.extract("year", Sobreaviso.data) == ano,
        )
        .order_by(Sobreaviso.data)
        .all()
    )
    # Gera lista de datas únicas ordenadas do mês com plantonistas
    datas_plantao = sorted({p.data for p in plantonistas})

    session_db.close()
    return render_template(
        "reports/consolidated_schedule.html",
        plantonistas=plantonistas,
        sobreavisos=sobreavisos,
        mes=mes,
        ano=ano,
        datas_plantao=datas_plantao,
    )


@report_bp.route("/list", methods=["GET"])
def consolidated_report():
    session_db = SessionLocal()
    mes = request.args.get("mes", default=datetime.now().month, type=int)
    ano = request.args.get("ano", default=datetime.now().year, type=int)
    plantonistas = (
        session_db.query(Plantonista)
        .options(
            joinedload(Plantonista.diurno_medico1),
            joinedload(Plantonista.diurno_medico2),
            joinedload(Plantonista.noturno_medico1),
            joinedload(Plantonista.noturno_medico2),
        )
        .filter(
            func.extract("month", Plantonista.data) == mes,
            func.extract("year", Plantonista.data) == ano,
        )
        .order_by(Plantonista.data)
        .all()
    )
    sobreavisos = (
        session_db.query(Sobreaviso)
        .options(joinedload(Sobreaviso.medico))
        .filter(
            func.extract("month", Sobreaviso.data) == mes,
            func.extract("year", Sobreaviso.data) == ano,
        )
        .order_by(Sobreaviso.data)
        .all()
    )
    # Ajustar headers e rows para refletir os nomes corretos do banco de dados
    plantonistas_headers = ["Data", "Diurno Médico 1",
                            "Diurno Médico 2", "Noturno Médico 1", "Noturno Médico 2"]
    plantonistas_data = [
        [
            p.data.strftime("%d/%m/%Y"),
            p.diurno_medico1.name if p.diurno_medico1 else "",
            p.diurno_medico2.name if p.diurno_medico2 else "",
            p.noturno_medico1.name if p.noturno_medico1 else "",
            p.noturno_medico2.name if p.noturno_medico2 else "",
        ]
        for p in plantonistas
    ]
    # Criar a variável days_and_weekdays com os dias e dias da semana
    days_and_weekdays = [
        (p.data.strftime("%d"), p.data.strftime("%A")) for p in plantonistas
    ]

    # Criar as variáveis diurno_rows e noturno_rows com os médicos escalados
    diurno_rows = [
        f"{p.diurno_medico1.name if p.diurno_medico1 else ''}, {p.diurno_medico2.name if p.diurno_medico2 else ''}"
        for p in plantonistas
    ]

    noturno_rows = [
        f"{p.noturno_medico1.name if p.noturno_medico1 else ''}, {p.noturno_medico2.name if p.noturno_medico2 else ''}"
        for p in plantonistas
    ]

    session_db.close()
    return render_template(
        "reports/consolidated_schedule.html",
        plantonistas_headers=plantonistas_headers,
        plantonistas_data=plantonistas_data,
        sobreavisos=sobreavisos,
        days_and_weekdays=days_and_weekdays,
        diurno_rows=diurno_rows,
        noturno_rows=noturno_rows,
        mes=mes,
        ano=ano,
    )
