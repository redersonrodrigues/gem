import pytest
import sqlalchemy
from app.core.database import SessionLocal, init_db
from app.models import Medico, Especializacao, Escala
from app.core.repositories import MedicoRepository, EspecializacaoRepository, EscalaRepository

def setup_module(module):
    init_db()

def test_especializacao_crud():
    db = SessionLocal()
    repo = EspecializacaoRepository(db)
    esp = Especializacao(nome="Teste Especialização")
    repo.create(esp)
    all_esps = repo.get_all()
    assert any(e.nome == "Teste Especialização" for e in all_esps)
    db.delete(esp)
    db.commit()
    db.close()

def test_medico_crud():
    db = SessionLocal()
    esp = Especializacao(nome="Esp CRUD")
    db.add(esp)
    db.commit()
    repo = MedicoRepository(db)
    medico = Medico(nome="Teste Médico", crm="99999", especialidade_id=esp.id)
    repo.create(medico)
    all_med = repo.get_all()
    assert any(m.nome == "Teste Médico" for m in all_med)
    db.delete(medico)
    db.delete(esp)
    db.commit()
    db.close()

def test_escala_crud():
    db = SessionLocal()
    esp = Especializacao(nome="Esp Escala")
    db.add(esp)
    db.commit()
    medico = Medico(nome="Médico Escala", crm="88888", especialidade_id=esp.id)
    db.add(medico)
    db.commit()
    repo = EscalaRepository(db)
    escala = Escala(medico_id=medico.id, dia_da_semana="Quarta", horario_inicio=None, horario_fim=None)
    repo.create(escala)
    all_esc = repo.get_all()
    assert any(e.dia_da_semana == "Quarta" for e in all_esc)
    db.delete(escala)
    db.delete(medico)
    db.delete(esp)
    db.commit()
    db.close()

def test_especializacao_crud_erro():
    db = SessionLocal()
    repo = EspecializacaoRepository(db)
    esp = Especializacao(nome=None)  # nome é obrigatório
    with pytest.raises(ValueError):
        repo.create(esp)
    db.rollback()
    db.close()

def test_medico_crud_erro_campos_obrigatorios():
    db = SessionLocal()
    repo = MedicoRepository(db)
    medico = Medico(nome=None, crm=None, especialidade_id=None)
    with pytest.raises(ValueError):
        repo.create(medico)
    db.rollback()
    db.close()

def test_medico_crud_erro_crm_duplicado():
    db = SessionLocal()
    # Limpeza das tabelas para garantir isolamento
    db.query(Medico).delete()
    db.query(Especializacao).delete()
    db.commit()
    esp = Especializacao(nome="Esp Teste")
    db.add(esp)
    db.commit()
    repo = MedicoRepository(db)
    medico1 = Medico(nome="A", crm="12345", especialidade_id=esp.id)
    repo.create(medico1)
    medico2 = Medico(nome="B", crm="12345", especialidade_id=esp.id)
    with pytest.raises(ValueError):
        repo.create(medico2)
    db.delete(medico1)
    db.delete(esp)
    db.commit()
    db.close()

def test_medico_crud_erro_especialidade_inexistente():
    db = SessionLocal()
    repo = MedicoRepository(db)
    medico = Medico(nome="C", crm="54321", especialidade_id=9999)
    with pytest.raises(ValueError):
        repo.create(medico)
    db.rollback()
    db.close()

def test_escala_crud_erro():
    db = SessionLocal()
    esp = Especializacao(nome="Esp Escala Erro")
    db.add(esp)
    db.commit()
    medico = Medico(nome="Médico Erro", crm="77777", especialidade_id=esp.id)
    db.add(medico)
    db.commit()
    repo = EscalaRepository(db)
    # Campos obrigatórios
    escala = Escala(medico_id=None, dia_da_semana=None, horario_inicio=None, horario_fim=None)
    with pytest.raises(ValueError):
        repo.create(escala)
    # Médico inexistente
    escala2 = Escala(medico_id=9999, dia_da_semana="Segunda", horario_inicio=None, horario_fim=None)
    with pytest.raises(ValueError):
        repo.create(escala2)
    db.delete(medico)
    db.delete(esp)
    db.commit()
    db.close()

def test_update_delete_invalid():
    db = SessionLocal()
    repo_esp = EspecializacaoRepository(db)
    repo_med = MedicoRepository(db)
    repo_esc = EscalaRepository(db)
    esp = Especializacao(nome="Esp Upd")
    repo_esp.create(esp)
    medico = Medico(nome="Med Upd", crm="upd1", especialidade_id=esp.id)
    repo_med.create(medico)
    escala = Escala(medico_id=medico.id, dia_da_semana="Domingo", horario_inicio=None, horario_fim=None)
    repo_esc.create(escala)
    # Update inválido
    medico.nome = None
    with pytest.raises(ValueError):
        repo_med.update(medico)
    escala.dia_da_semana = None
    with pytest.raises(ValueError):
        repo_esc.update(escala)
    # Delete de objeto não persistido
    fake_esp = Especializacao(nome="Fake")
    with pytest.raises(Exception):
        repo_esp.delete(fake_esp)
    db.delete(escala)
    db.delete(medico)
    db.delete(esp)
    db.commit()
    db.close()
