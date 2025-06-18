from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.models.database import init_db, SessionLocal
from app.models.user import User
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from app.models.log import Log
from app.models.schedule import Schedule
from app.config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from datetime import timezone
from sqlalchemy.orm import joinedload
from app.controllers.plantonista_controller import plantonista_bp
from app.controllers.sobreaviso_controller import sobreaviso_bp
from app.controllers.report_controller import report_bp
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from app.models.notification_manager import NotificationManager


# Decorator para exigir login
def login_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


# Decorator para exigir admin
def admin_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Acesso restrito ao administrador.", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)

    return decorated_function


app = Flask(__name__, template_folder="app/views", static_folder="static")
app.secret_key = "sua-chave-secreta"
app.register_blueprint(plantonista_bp)
app.register_blueprint(sobreaviso_bp)
app.register_blueprint(report_bp)


@app.before_request
def initialize_database():
    init_db()


@app.route("/")
@login_required
def home():
    return render_template("home.html")


@app.route("/doctors", methods=["GET", "POST"])
@admin_required
@login_required
def doctors():
    session_db = SessionLocal()
    if request.method == "POST":
        name = request.form["name"].strip().upper()
        fantasy_name = request.form["fantasy_name"].strip().upper()
        specialization_ids = request.form.getlist("specializations")
        # Verifica nome único
        if session_db.query(Doctor).filter_by(name=name).first():
            flash("Já existe um médico com esse nome.", "danger")
        else:
            doctor = Doctor(name=name, fantasy_name=fantasy_name)
            # Adiciona especializações
            doctor.specializations = (
                session_db.query(Specialization)
                .filter(Specialization.id.in_(specialization_ids))
                .all()
            )
            session_db.add(doctor)
            session_db.commit()
            # Log da ação
            log = Log(
                user_id=session["user_id"],
                action="CREATE",
                entity="Doctor",
                entity_id=doctor.id,
                timestamp=datetime.datetime.now(timezone.utc),
            )
            session_db.add(log)
            session_db.commit()
            flash("Médico cadastrado com sucesso!", "success")
        return redirect(url_for("doctors"))
    doctors = session_db.query(Doctor).options(
        joinedload(Doctor.specializations)).all()
    specializations = session_db.query(Specialization).all()
    session_db.close()
    return render_template(
        "doctor_form.html", doctors=doctors, specializations=specializations
    )


@app.route("/doctors/delete/<int:doctor_id>", methods=["POST"])
@admin_required
@login_required
def delete_doctor(doctor_id):
    session_db = SessionLocal()
    doctor = session_db.query(Doctor).get(doctor_id)
    if doctor:
        session_db.delete(doctor)
        session_db.commit()
        # Log da ação
        log = Log(
            user_id=session["user_id"],
            action="DELETE",
            entity="Doctor",
            entity_id=doctor_id,
            timestamp=datetime.datetime.now(timezone.utc),
        )
        session_db.add(log)
        session_db.commit()
        flash("Médico removido com sucesso!", "success")
    else:
        flash("Médico não encontrado.", "danger")
    session_db.close()
    return redirect(url_for("doctors"))


@app.route("/doctors/edit/<int:doctor_id>", methods=["GET", "POST"])
@admin_required
@login_required
def edit_doctor(doctor_id):
    session_db = SessionLocal()
    doctor = session_db.query(Doctor).get(doctor_id)
    specializations = session_db.query(Specialization).all()
    if not doctor:
        flash("Médico não encontrado.", "danger")
        session_db.close()
        return redirect(url_for("doctors"))
    if request.method == "POST":
        name = request.form["name"].strip().upper()
        fantasy_name = request.form["fantasy_name"].strip().upper()
        specialization_ids = request.form.getlist("specializations")
        # Verifica nome único (exceto o próprio)
        if (
            session_db.query(Doctor)
            .filter(Doctor.name == name, Doctor.id != doctor_id)
            .first()
        ):
            flash("Já existe um médico com esse nome.", "danger")
        else:
            doctor.name = name
            doctor.fantasy_name = fantasy_name
            # Atualiza especializações
            doctor.specializations = (
                session_db.query(Specialization)
                .filter(Specialization.id.in_(specialization_ids))
                .all()
            )
            session_db.commit()
            # Log da ação
            log = Log(
                user_id=session["user_id"],
                action="UPDATE",
                entity="Doctor",
                entity_id=doctor.id,
                timestamp=datetime.datetime.now(timezone.utc),
            )
            session_db.add(log)
            session_db.commit()
            flash("Médico atualizado com sucesso!", "success")
            return redirect(url_for("doctors"))
    response = render_template(
        "doctor_form.html", edit_doctor=doctor, specializations=specializations
    )
    session_db.close()
    return response


@app.route("/specializations", methods=["GET", "POST"])
@admin_required
@login_required
def specializations():
    session_db = SessionLocal()
    if request.method == "POST":
        try:
            name = request.form["name"].strip().upper()
            # Verifica nome único
            if session_db.query(Specialization).filter_by(name=name).first():
                flash("Já existe uma especialização com esse nome.", "danger")
            else:
                specialization = Specialization(name=name)
                session_db.add(specialization)
                session_db.commit()
                # Log da ação
                log = Log(
                    user_id=session["user_id"],
                    action="CREATE",
                    entity="Specialization",
                    entity_id=specialization.id,
                    timestamp=datetime.datetime.now(timezone.utc),
                )
                session_db.add(log)
                session_db.commit()
                flash("Especialização cadastrada com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao cadastrar especialização: {str(e)}", "danger")
        finally:
            session_db.close()
        return redirect(url_for("specializations"))
    specializations = session_db.query(Specialization).all()
    session_db.close()
    # Transformar objetos em uma lista de listas
    specializations_data = [
        [spec.id, spec.name] for spec in specializations
    ]
    return render_template("specialization_form.html", specializations=specializations_data)


@app.route("/specializations/delete/<int:spec_id>", methods=["POST"])
@admin_required
@login_required
def delete_specialization(spec_id):
    session_db = SessionLocal()
    spec = session_db.query(Specialization).get(spec_id)
    if spec:
        session_db.delete(spec)
        session_db.commit()
        # Log da ação
        log = Log(
            user_id=session["user_id"],
            action="DELETE",
            entity="Specialization",
            entity_id=spec_id,
            timestamp=datetime.datetime.now(timezone.utc),
        )
        session_db.add(log)
        session_db.commit()
        flash("Especialização removida com sucesso!", "success")
    else:
        flash("Especialização não encontrada.", "danger")
    session_db.close()
    return redirect(url_for("specializations"))


@app.route("/specializations/edit/<int:spec_id>", methods=["GET", "POST"])
@admin_required
@login_required
def edit_specialization(spec_id):
    session_db = SessionLocal()
    spec = session_db.query(Specialization).get(spec_id)
    if not spec:
        flash("Especialização não encontrada.", "danger")
        session_db.close()
        return redirect(url_for("specializations"))
    if request.method == "POST":
        name = request.form["name"].strip().upper()
        # Verifica nome único (exceto o próprio)
        if (
            session_db.query(Specialization)
            .filter(Specialization.name == name, Specialization.id != spec_id)
            .first()
        ):
            flash("Já existe uma especialização com esse nome.", "danger")
        else:
            spec.name = name
            session_db.commit()
            # Log da ação
            log = Log(
                user_id=session["user_id"],
                action="UPDATE",
                entity="Specialization",
                entity_id=spec.id,
                timestamp=datetime.datetime.now(timezone.utc),
            )
            session_db.add(log)
            session_db.commit()
            flash("Especialização atualizada com sucesso!", "success")
            session_db.close()
            return redirect(url_for("specializations"))
    session_db.close()
    return render_template("specialization_form.html", edit_specialization=spec)


@app.route("/schedules", methods=["GET", "POST"])
@login_required
def schedules():
    session_db = SessionLocal()
    if request.method == "POST":
        data_escala = request.form.get("data_escala")
        tipo = request.form.get("tipo")
        if tipo == "PLANTONISTA":
            diurno_medico1_id = request.form["diurno_medico1_id"]
            diurno_medico2_id = request.form["diurno_medico2_id"]
            noturno_medico1_id = request.form["noturno_medico1_id"]
            noturno_medico2_id = request.form["noturno_medico2_id"]
            # Validação: todos os campos obrigatórios e IDs distintos
            if not all(
                [
                    diurno_medico1_id,
                    diurno_medico2_id,
                    noturno_medico1_id,
                    noturno_medico2_id,
                ]
            ):
                flash("Todos os campos de médicos devem ser preenchidos.", "danger")
            elif (
                len(
                    {
                        diurno_medico1_id,
                        diurno_medico2_id,
                        noturno_medico1_id,
                        noturno_medico2_id,
                    }
                )
                < 4
            ):
                flash("Os médicos de cada turno devem ser distintos.", "danger")
            elif (
                session_db.query(Schedule)
                .filter_by(data=data_escala, tipo=tipo)
                .first()
            ):
                flash("Já existe escala para este dia.", "danger")
            else:
                escala = Schedule(
                    data=data_escala,
                    tipo=tipo,
                    diurno_medico1_id=diurno_medico1_id,
                    diurno_medico2_id=diurno_medico2_id,
                    noturno_medico1_id=noturno_medico1_id,
                    noturno_medico2_id=noturno_medico2_id,
                )
                session_db.add(escala)
                session_db.commit()
                log = Log(
                    user_id=session["user_id"],
                    action="CREATE",
                    entity="Schedule",
                    entity_id=escala.id,
                    timestamp=datetime.datetime.now(timezone.utc),
                )
                session_db.add(log)
                session_db.commit()
                flash("Escala cadastrada com sucesso!", "success")
        elif tipo == "SOBREAVISO":
            especialidade = request.form["especialidade_sobreaviso"].strip(
            ).upper()
            data_inicio = request.form["data_inicio"]
            periodo = request.form["periodo"]
            medico_id = request.form["medico_sobreaviso"]
            if not all([especialidade, data_inicio, periodo, medico_id]):
                flash("Todos os campos de sobreaviso são obrigatórios.", "danger")
            else:
                data_inicio_dt = datetime.datetime.strptime(
                    data_inicio, "%Y-%m-%d"
                ).date()
                if especialidade == "ORTOPEDIA" and periodo == "quinzenal":
                    for quinzena in [(1, 15), (16, 31)]:
                        data_quinzena = data_inicio_dt.replace(day=quinzena[0])
                        existe = (
                            session_db.query(Schedule)
                            .filter_by(
                                tipo=tipo,
                                sobreaviso_especialidade=especialidade,
                                data=data_quinzena,
                                sobreaviso_medico_id=medico_id,
                            )
                            .first()
                        )
                        if not existe:
                            escala = Schedule(
                                data=data_quinzena,
                                tipo=tipo,
                                sobreaviso_especialidade=especialidade,
                                sobreaviso_medico_id=medico_id,
                            )
                            session_db.add(escala)
                elif periodo == "semanal":
                    for semana in range(5):
                        data_semana = data_inicio_dt + datetime.timedelta(
                            days=semana * 7
                        )
                        existe = (
                            session_db.query(Schedule)
                            .filter_by(
                                tipo=tipo,
                                sobreaviso_especialidade=especialidade,
                                data=data_semana,
                                sobreaviso_medico_id=medico_id,
                            )
                            .first()
                        )
                        if not existe:
                            escala = Schedule(
                                data=data_semana,
                                tipo=tipo,
                                sobreaviso_especialidade=especialidade,
                                sobreaviso_medico_id=medico_id,
                            )
                            session_db.add(escala)
                session_db.commit()
                flash("Escala de sobreaviso cadastrada!", "success")
        return redirect(url_for("schedules"))
    escalas = session_db.query(Schedule).all()
    doctors = session_db.query(Doctor).all()
    specializations = session_db.query(Specialization).all()
    session_db.close()
    return render_template(
        "schedule_view.html",
        escalas=escalas,
        doctors=doctors,
        specializations=specializations,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session_db = SessionLocal()
        user = session_db.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["is_admin"] = user.is_admin
            session["username"] = user.username
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuário ou senha inválidos.", "danger")
        session_db.close()
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("login"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestão de Escalas de Plantonistas")

        # Layout principal
        layout = QVBoxLayout()

        # Botões de exemplo
        btn_create = QPushButton("Cadastrar Plantonista")
        btn_create.clicked.connect(self.create_plantonista)
        layout.addWidget(btn_create)

        btn_list = QPushButton("Listar Plantonistas")
        btn_list.clicked.connect(self.list_plantonistas)
        layout.addWidget(btn_list)

        # Configurar o widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_plantonista(self):
        NotificationManager.success(
            "Funcionalidade de cadastro em desenvolvimento.")

    def list_plantonistas(self):
        NotificationManager.info(
            "Funcionalidade de listagem em desenvolvimento.")


# Remover a função create_app e rodar diretamente o app já configurado

if __name__ == "__main__":
    app.run(debug=True)
