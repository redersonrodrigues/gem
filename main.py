from flask import Flask, render_template, request, redirect, url_for
from app.config import Config
from app.models.database import init_db, SessionLocal
from app.models.doctor import Doctor
from app.models.specialization import Specialization
import os

app = Flask(__name__, template_folder="app/views", static_folder="static")


@app.before_first_request
def initialize_database():
    init_db()


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    session = SessionLocal()
    if request.method == 'POST':
        name = request.form['name']
        specialization_id = request.form['specialization_id']
        doctor = Doctor(name=name, specialization_id=specialization_id)
        session.add(doctor)
        session.commit()
        return redirect(url_for('doctors'))
    doctors = session.query(Doctor).all()
    specializations = session.query(Specialization).all()
    return render_template('doctor_form.html', doctors=doctors, specializations=specializations)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.controllers import main as main_controller

    app.register_blueprint(main_controller)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
