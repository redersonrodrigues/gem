from app.core.database import SessionLocal
from app.models import Medico, Especializacao, Escala
from app.core.repositories import MedicoRepository, EspecializacaoRepository, EscalaRepository

def main():
    db = SessionLocal()
    # CRUD Especialização
    esp_repo = EspecializacaoRepository(db)
    esp = Especializacao(nome="Clínica Geral")
    esp_repo.create(esp)
    print("Especializações:", esp_repo.get_all())

    # CRUD Médico
    med_repo = MedicoRepository(db)
    medico = Medico(nome="Dr. João", crm="12345", especialidade_id=esp.id)
    med_repo.create(medico)
    print("Médicos:", med_repo.get_all())

    # CRUD Escala
    esc_repo = EscalaRepository(db)
    escala = Escala(medico_id=medico.id, dia_da_semana="Segunda", horario_inicio=None, horario_fim=None)
    esc_repo.create(escala)
    print("Escalas:", esc_repo.get_all())

    db.close()

if __name__ == "__main__":
    main()
