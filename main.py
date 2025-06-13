from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.config import Config
from app.models.database import init_db, SessionLocal
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import os
import datetime

app = Flask(__name__, template_folder="app/views", static_folder="static")
app.secret_key = 'sua-chave-secreta'


@app.before_first_request
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
        name = request.form["name"]
        specialization_id = request.form["specialization_id"]
        doctor = Doctor(name=name, specialization_id=specialization_id)
        session_db.add(doctor)
        session_db.commit()
        return redirect(url_for("doctors"))
    doctors = session_db.query(Doctor).all()
    specializations = session_db.query(Specialization).all()
    return render_template(
        "doctor_form.html", doctors=doctors, specializations=specializations
    )


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
    # Implementação CRUD para escalas
    pass


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
