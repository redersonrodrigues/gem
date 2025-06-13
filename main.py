from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.config import Config
from app.models.database import init_db, SessionLocal
from app.models.doctor import Doctor
from app.models.log import Log
from app.models.specialization import Specialization
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import os
import datetime
from datetime import datetime

app = Flask(__name__, template_folder="app/views", static_folder="static")
app.secret_key = 'sua-chave-secreta'


@app.before_first_request
def initialize_database():
    init_db()


@app.route("/")
@login_required
def home():
    return render_template("home.html")


@app.route('/doctors', methods=['GET', 'POST'])
@admin_required
@login_required
def doctors():
    session_db = SessionLocal()
    if request.method == 'POST':
        name = request.form['name'].strip().upper()
        specialization_id = request.form['specialization_id']
        # Verifica nome único
        if session_db.query(Doctor).filter_by(name=name).first():
            flash('Já existe um médico com esse nome.', 'danger')
        else:
            doctor = Doctor(name=name, specialization_id=specialization_id)
            session_db.add(doctor)
            session_db.commit()
            # Log da ação
            log = Log(user_id=session['user_id'], action='CREATE', entity='Doctor', entity_id=doctor.id, timestamp=datetime.utcnow())
            session_db.add(log)
            session_db.commit()
            flash('Médico cadastrado com sucesso!', 'success')
        return redirect(url_for('doctors'))
    doctors = session_db.query(Doctor).all()
    specializations = session_db.query(app.models.specialization.Specialization).all()
    session_db.close()
    return render_template('doctor_form.html', doctors=doctors, specializations=specializations)


@app.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
@admin_required
@login_required
def delete_doctor(doctor_id):
    session_db = SessionLocal()
    doctor = session_db.query(Doctor).get(doctor_id)
    if doctor:
        session_db.delete(doctor)
        session_db.commit()
        # Log da ação
        log = Log(user_id=session['user_id'], action='DELETE', entity='Doctor', entity_id=doctor_id, timestamp=datetime.utcnow())
        session_db.add(log)
        session_db.commit()
        flash('Médico removido com sucesso!', 'success')
    else:
        flash('Médico não encontrado.', 'danger')
    session_db.close()
    return redirect(url_for('doctors'))


@app.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_doctor(doctor_id):
    session_db = SessionLocal()
    doctor = session_db.query(Doctor).get(doctor_id)
    specializations = session_db.query(app.models.specialization.Specialization).all()
    if not doctor:
        flash('Médico não encontrado.', 'danger')
        session_db.close()
        return redirect(url_for('doctors'))
    if request.method == 'POST':
        name = request.form['name'].strip().upper()
        specialization_id = request.form['specialization_id']
        # Verifica nome único (exceto o próprio)
        if session_db.query(Doctor).filter(Doctor.name == name, Doctor.id != doctor_id).first():
            flash('Já existe um médico com esse nome.', 'danger')
        else:
            doctor.name = name
            doctor.specialization_id = specialization_id
            session_db.commit()
            # Log da ação
            log = Log(user_id=session['user_id'], action='UPDATE', entity='Doctor', entity_id=doctor.id, timestamp=datetime.utcnow())
            session_db.add(log)
            session_db.commit()
            flash('Médico atualizado com sucesso!', 'success')
            session_db.close()
            return redirect(url_for('doctors'))
    session_db.close()
    return render_template('doctor_form.html', edit_doctor=doctor, specializations=specializations)


@app.route('/specializations', methods=['GET', 'POST'])
@admin_required
@login_required
def specializations():
    # Implementação CRUD para especializações
    pass


@app.route('/schedules', methods=['GET', 'POST'])
@login_required
def schedules():
    # Permitir cadastro/alteração apenas até o dia 15 do mês seguinte para usuários comuns
    if not session.get('is_admin') and request.method == 'POST':
        today = datetime.today()
        # Limite: dia 15 do mês seguinte
        limite = datetime(today.year, today.month, 15)
        if today.day > 15:
            # Se já passou do dia 15, só pode cadastrar para o mês seguinte
            if 'data_escala' in request.form:
                data_escala = datetime.strptime(request.form['data_escala'], '%Y-%m-%d')
                proximo_mes = today.month + 1 if today.month < 12 else 1
                ano = today.year if today.month < 12 else today.year + 1
                limite = datetime(ano, proximo_mes, 15)
                if data_escala > limite:
                    flash('Usuário comum só pode cadastrar/alterar escalas até o dia 15 do mês seguinte.', 'danger')
                    return redirect(url_for('schedules'))
        else:
            if 'data_escala' in request.form:
                data_escala = datetime.strptime(request.form['data_escala'], '%Y-%m-%d')
                if data_escala > limite:
                    flash('Usuário comum só pode cadastrar/alterar escalas até o dia 15 do mês seguinte.', 'danger')
                    return redirect(url_for('schedules'))
    # ...restante do CRUD de escalas...
    return render_template('schedule_view.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session_db = SessionLocal()
        user = session_db.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            session['username'] = user.username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
        session_db.close()
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))


# Decorator para exigir login
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Decorator para exigir admin
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Acesso restrito ao administrador.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.controllers import main as main_controller

    app.register_blueprint(main_controller)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
