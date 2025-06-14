from flask import Blueprint, render_template
from app.models.sobreaviso import Sobreaviso
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from app.models.database import SessionLocal

sobreaviso_bp = Blueprint('sobreavisos', __name__, url_prefix='/sobreavisos')

@sobreaviso_bp.route('/')
def list_sobreavisos():
    session_db = SessionLocal()
    sobreavisos = session_db.query(Sobreaviso).all()
    doctors = session_db.query(Doctor).all()
    specializations = session_db.query(Specialization).all()
    session_db.close()
    return render_template('sobreavisos/list.html', sobreavisos=sobreavisos, doctors=doctors, specializations=specializations)