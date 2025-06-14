from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.models.database import init_db, SessionLocal
from app.models.user import User
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from app.models.schedule import Schedule
from app.models.log import Log
from app.config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

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

app = Flask(__name__, template_folder="app/views", static_folder="static")
app.secret_key = 'sua-chave-secreta'


@app.before_request
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
            log = Log(user_id=session['user_id'], action='CREATE', entity='Doctor', entity_id=doctor.id, timestamp=datetime.datetime.utcnow())
            session_db.add(log)
            session_db.commit()
            flash('Médico cadastrado com sucesso!', 'success')
        return redirect(url_for('doctors'))
    doctors = session_db.query(Doctor).all()
    specializations = session_db.query(Specialization).all()
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
        log = Log(user_id=session['user_id'], action='DELETE', entity='Doctor', entity_id=doctor_id, timestamp=datetime.datetime.utcnow())
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
            log = Log(user_id=session['user_id'], action='UPDATE', entity='Doctor', entity_id=doctor.id, timestamp=datetime.datetime.utcnow())
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
    session_db = SessionLocal()
    if request.method == 'POST':
        name = request.form['name'].strip().upper()
        # Verifica nome único
        if session_db.query(Specialization).filter_by(name=name).first():
            flash('Já existe uma especialização com esse nome.', 'danger')
        else:
            specialization = Specialization(name=name)
            session_db.add(specialization)
            session_db.commit()
            # Log da ação
            log = Log(user_id=session['user_id'], action='CREATE', entity='Specialization', entity_id=specialization.id, timestamp=datetime.datetime.utcnow())
            session_db.add(log)
            session_db.commit()
            flash('Especialização cadastrada com sucesso!', 'success')
        return redirect(url_for('specializations'))
    specializations = session_db.query(Specialization).all()
    session_db.close()
    return render_template('specialization_form.html', specializations=specializations)


@app.route('/specializations/delete/<int:spec_id>', methods=['POST'])
@admin_required
@login_required
def delete_specialization(spec_id):
    session_db = SessionLocal()
    spec = session_db.query(Specialization).get(spec_id)
    if spec:
        session_db.delete(spec)
        session_db.commit()
        # Log da ação
        log = Log(user_id=session['user_id'], action='DELETE', entity='Specialization', entity_id=spec_id, timestamp=datetime.datetime.utcnow())
        session_db.add(log)
        session_db.commit()
        flash('Especialização removida com sucesso!', 'success')
    else:
        flash('Especialização não encontrada.', 'danger')
    session_db.close()
    return redirect(url_for('specializations'))


@app.route('/specializations/edit/<int:spec_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_specialization(spec_id):
    session_db = SessionLocal()
    spec = session_db.query(Specialization).get(spec_id)
    if not spec:
        flash('Especialização não encontrada.', 'danger')
        session_db.close()
        return redirect(url_for('specializations'))
    if request.method == 'POST':
        name = request.form['name'].strip().upper()
        # Verifica nome único (exceto o próprio)
        if session_db.query(Specialization).filter(Specialization.name == name, Specialization.id != spec_id).first():
            flash('Já existe uma especialização com esse nome.', 'danger')
        else:
            spec.name = name
            session_db.commit()
            # Log da ação
            log = Log(user_id=session['user_id'], action='UPDATE', entity='Specialization', entity_id=spec.id, timestamp=datetime.datetime.utcnow())
            session_db.add(log)
            session_db.commit()
            flash('Especialização atualizada com sucesso!', 'success')
            session_db.close()
            return redirect(url_for('specializations'))
    session_db.close()
    return render_template('specialization_form.html', edit_specialization=spec)


@app.route('/schedules', methods=['GET', 'POST'])
@login_required
def schedules():
    session_db = SessionLocal()
    if request.method == 'POST':
        # Respeita restrição de datas para usuários comuns (já implementada anteriormente)
        data_escala = request.form['data_escala']
        tipo = request.form['tipo']
        # Exemplo: cadastro de escala plantonista
        if tipo == 'PLANTONISTA':
            medico1_id = request.form['medico1_id']
            medico2_id = request.form['medico2_id']
            # Verifica se já existe escala para o dia
            if session_db.query(Schedule).filter_by(data=data_escala, tipo=tipo).first():
                flash('Já existe escala para este dia.', 'danger')
            else:
                escala = Schedule(data=data_escala, tipo=tipo, medico1_id=medico1_id, medico2_id=medico2_id)
                session_db.add(escala)
                session_db.commit()
                # Log da ação
                log = Log(user_id=session['user_id'], action='CREATE', entity='Schedule', entity_id=escala.id, timestamp=datetime.datetime.utcnow())
                session_db.add(log)
                session_db.commit()
                flash('Escala cadastrada com sucesso!', 'success')
        # ...demais tipos de escala...
        return redirect(url_for('schedules'))
    escalas = session_db.query(Schedule).all()
    doctors = session_db.query(Doctor).all()
    session_db.close()
    return render_template('schedule_view.html', escalas=escalas, doctors=doctors)


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


# Remover a função create_app e rodar diretamente o app já configurado

if __name__ == "__main__":
    app.run(debug=True)
