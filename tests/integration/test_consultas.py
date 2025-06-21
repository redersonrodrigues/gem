import pytest
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.core.consulta_medicos_disponiveis import medicos_disponiveis_por_especializacao_periodo
from app.core.consulta_escalas_mes import consultar_escalas_mes
from app.core.consulta_medicos_mais_plantao import medicos_mais_plantao
from app.core.consulta_medicos_sem_escalas import medicos_sem_escalas
from app.core.cobertura_especialidades_por_turno import cobertura_especialidades_por_turno
from app.models.usuario import Usuario
from app.core.consulta_medicos_inativos_afastados import medicos_inativos_afastados
from app.core.consulta_escalas_conflitos import escalas_com_conflitos
from app.core.relatorio_escala_plantonistas import dados_escala_plantonistas, exportar_csv, exportar_pdf
from app.core.relatorio_escala_sobreaviso import consultar_sobreaviso_mes, exportar_csv as exportar_csv_sobreaviso, exportar_pdf as exportar_pdf_sobreaviso
from app.core.relatorio_carga_horaria_medico import consulta_carga_horaria_por_medico, exportar_carga_horaria_csv, exportar_carga_horaria_pdf
import os

@pytest.fixture(autouse=True)
def limpar_tabelas(session):
    # Limpa as tabelas relevantes antes de cada teste
    session.query(EscalaPlantonista).delete()
    session.query(EscalaSobreaviso).delete()
    session.query(Medico).delete()
    session.query(Especializacao).delete()
    session.commit()

@pytest.fixture
def setup_db(session):
    # Cria especialização
    esp = Especializacao(nome="Cardiologia")
    session.add(esp)
    session.commit()
    # Cria médicos
    m1 = Medico(nome="Dr. A", status="ativo", especializacao_id=esp.id)
    m2 = Medico(nome="Dr. B", status="ativo", especializacao_id=esp.id)
    m3 = Medico(nome="Dr. C", status="ativo", especializacao_id=esp.id)
    session.add_all([m1, m2, m3])
    session.commit()
    return esp, [m1, m2, m3]

def test_medicos_disponiveis_sem_escalas(session, setup_db):
    esp, medicos = setup_db
    disponiveis = medicos_disponiveis_por_especializacao_periodo(
        session, esp.id, date(2024, 6, 1), date(2024, 6, 30)
    )
    assert set([m.id for m in disponiveis]) == set([m.id for m in medicos])

def test_medicos_disponiveis_com_plantao(session, setup_db):
    esp, medicos = setup_db
    # Escala Dr. A em plantão
    escala = EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno")
    session.add(escala)
    session.commit()
    disponiveis = medicos_disponiveis_por_especializacao_periodo(
        session, esp.id, date(2024, 6, 1), date(2024, 6, 30)
    )
    ids = [m.id for m in disponiveis]
    assert medicos[0].id not in ids
    assert medicos[1].id in ids and medicos[2].id in ids

def test_medicos_disponiveis_com_sobreaviso(session, setup_db):
    esp, medicos = setup_db
    # Escala Dr. B em sobreaviso
    sobreaviso = EscalaSobreaviso(medico1_id=medicos[1].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 20))
    session.add(sobreaviso)
    session.commit()
    disponiveis = medicos_disponiveis_por_especializacao_periodo(
        session, esp.id, date(2024, 6, 1), date(2024, 6, 30)
    )
    ids = [m.id for m in disponiveis]
    assert medicos[1].id not in ids
    assert medicos[0].id in ids and medicos[2].id in ids

def test_medicos_disponiveis_todos_escalados(session, setup_db):
    esp, medicos = setup_db
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaSobreaviso(medico1_id=medicos[1].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 20)))
    session.add(EscalaPlantonista(medico1_id=medicos[2].id, data=date(2024, 6, 15), turno="diurno"))
    session.commit()
    disponiveis = medicos_disponiveis_por_especializacao_periodo(
        session, esp.id, date(2024, 6, 1), date(2024, 6, 30)
    )
    assert disponiveis == []

def test_consultar_escalas_mes(session, setup_db):
    esp, medicos = setup_db
    # Plantão Dr. A dia 10, Dr. B dia 15
    p1 = EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno")
    p2 = EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 6, 15), turno="noturno")
    session.add_all([p1, p2])
    # Sobreaviso Dr. A de 5 a 20
    s1 = EscalaSobreaviso(medico1_id=medicos[0].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 20))
    session.add(s1)
    session.commit()
    # Consulta geral
    resultado = consultar_escalas_mes(session, 2024, 6)
    assert len(resultado["plantao"]) == 2
    assert len(resultado["sobreaviso"]) == 1
    # Consulta filtrando por médico
    resultado_m1 = consultar_escalas_mes(session, 2024, 6, medico_id=medicos[0].id)
    assert all(p.medico1_id == medicos[0].id or p.medico2_id == medicos[0].id for p in resultado_m1["plantao"])
    assert all(s.medico1_id == medicos[0].id for s in resultado_m1["sobreaviso"])
    # Consulta filtrando por especialização
    resultado_esp = consultar_escalas_mes(session, 2024, 6, especializacao_id=esp.id)
    assert all(p.medico1.especializacao_id == esp.id for p in resultado_esp["plantao"])
    assert all(s.especializacao_id == esp.id for s in resultado_esp["sobreaviso"])

def test_medicos_mais_plantao(session, setup_db):
    esp, medicos = setup_db
    # Dr. A: 2 plantões, Dr. B: 1 plantão, Dr. C: 0
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 12), turno="noturno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 6, 15), turno="diurno"))
    session.commit()
    resultado = medicos_mais_plantao(session, date(2024, 6, 1), date(2024, 6, 30))
    assert resultado[0].id == medicos[0].id
    assert resultado[0].total_plantao == 2
    assert resultado[1].id == medicos[1].id
    assert resultado[1].total_plantao == 1
    # Testa filtro por especialização
    resultado_esp = medicos_mais_plantao(session, date(2024, 6, 1), date(2024, 6, 30), especializacao_id=esp.id)
    assert all(r.id in [m.id for m in medicos] for r in resultado_esp)

def test_medicos_sem_escalas(session, setup_db):
    esp, medicos = setup_db
    # Todos sem escala
    resultado = medicos_sem_escalas(session, date(2024, 6, 1), date(2024, 6, 30))
    assert set([m.id for m in resultado]) == set([m.id for m in medicos])
    # Dr. A recebe plantão
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.commit()
    resultado2 = medicos_sem_escalas(session, date(2024, 6, 1), date(2024, 6, 30))
    ids2 = [m.id for m in resultado2]
    assert medicos[0].id not in ids2
    assert medicos[1].id in ids2 and medicos[2].id in ids2
    # Dr. B recebe sobreaviso
    session.add(EscalaSobreaviso(medico1_id=medicos[1].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 20)))
    session.commit()
    resultado3 = medicos_sem_escalas(session, date(2024, 6, 1), date(2024, 6, 30))
    ids3 = [m.id for m in resultado3]
    assert medicos[0].id not in ids3
    assert medicos[1].id not in ids3
    assert medicos[2].id in ids3
    # Testa filtro por especialização
    resultado_esp = medicos_sem_escalas(session, date(2024, 6, 1), date(2024, 6, 30), especializacao_id=esp.id)
    assert all(m.especializacao_id == esp.id for m in resultado_esp)

def test_cobertura_especialidades_por_turno(session, setup_db):
    esp, medicos = setup_db
    # Cria plantão apenas para Dr. A em 10/06 diurno
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.commit()
    lacunas = cobertura_especialidades_por_turno(session, date(2024, 6, 10), date(2024, 6, 11))
    # Deve faltar noturno do dia 10 e ambos turnos do dia 11
    datas_turnos = set((l[2], l[3]) for l in lacunas)
    assert (date(2024, 6, 10), "noturno") in datas_turnos
    assert (date(2024, 6, 11), "diurno") in datas_turnos
    assert (date(2024, 6, 11), "noturno") in datas_turnos
    # Não deve faltar diurno do dia 10
    assert (date(2024, 6, 10), "diurno") not in datas_turnos

def test_consulta_historico_escalas(session, usuario_admin, escala_plantonista):
    from app.core.consulta_historico_escalas import consultar_historico_escalas
    from app.models.audit_log import AuditLog
    import datetime

    # Simula alteração na escala
    escala_plantonista.turno = 'noturno'
    session.commit()
    # Consulta histórico
    historico = consultar_historico_escalas(session, escala_plantonista.id, 'plantonista')
    assert len(historico) >= 1
    assert any('turno' in (h['alteracoes'] or '') for h in historico)
    assert all('acao' in h and 'usuario' in h and 'data' in h for h in historico)

def test_medicos_inativos_afastados(session, setup_db):
    esp, medicos = setup_db
    # Dr. A ativo, Dr. B inativo, Dr. C ativo
    medicos[1].status = 'inativo'
    session.commit()
    # Dr. C sem escalas, Dr. A recebe plantão
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.commit()
    resultado = medicos_inativos_afastados(
        session, date(2024, 6, 1), date(2024, 6, 30)
    )
    ids_inativos = [m.id for m in resultado['inativos']]
    ids_afastados = [m.id for m in resultado['afastados']]
    assert medicos[1].id in ids_inativos
    assert medicos[2].id in ids_afastados
    assert medicos[0].id not in ids_afastados
    assert medicos[0].id not in ids_inativos

def test_escalas_com_conflitos(session, setup_db):
    esp, medicos = setup_db
    # Dr. A: plantão e sobreaviso no mesmo dia (conflito plantão-sobreaviso)
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaSobreaviso(medico1_id=medicos[0].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 10), data_final=date(2024, 6, 15)))
    # Dr. B: sobreaviso sobreposto
    session.add(EscalaSobreaviso(medico1_id=medicos[1].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 15)))
    session.add(EscalaSobreaviso(medico1_id=medicos[1].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 10), data_final=date(2024, 6, 20)))
    session.commit()
    conflitos = escalas_com_conflitos(session, date(2024, 6, 1), date(2024, 6, 30))
    tipos = [c['tipo'] for c in conflitos]
    assert 'sobreaviso-sobreaviso' in tipos
    assert 'plantao-sobreaviso' in tipos

def test_relatorio_escala_plantonistas_csv_pdf(tmp_path, session, setup_db):
    esp, medicos = setup_db
    # Cria plantões
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 6, 15), turno="noturno"))
    session.commit()
    dados = dados_escala_plantonistas(session, 2024, 6)
    # Exporta CSV
    csv_path = os.path.join(tmp_path, 'relatorio_plantonistas.csv')
    exportar_csv(dados, csv_path)
    assert os.path.exists(csv_path)
    with open(csv_path, encoding='utf-8') as f:
        linhas = f.readlines()
    assert 'Dr. A' in ''.join(linhas) and 'Dr. B' in ''.join(linhas)
    # Exporta PDF
    pdf_path = os.path.join(tmp_path, 'relatorio_plantonistas.pdf')
    exportar_pdf(dados, pdf_path)
    assert os.path.exists(pdf_path)

def test_relatorio_escala_sobreaviso_csv_pdf(tmp_path, session, setup_db):
    esp, medicos = setup_db
    # Cria sobreavisos
    session.add(EscalaSobreaviso(medico1_id=medicos[0].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 10)))
    session.add(EscalaSobreaviso(medico1_id=medicos[1].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 15), data_final=date(2024, 6, 20)))
    session.commit()
    dados = consultar_sobreaviso_mes(session, 2024, 6)
    # Exporta CSV
    csv_path = os.path.join(tmp_path, 'relatorio_sobreaviso.csv')
    exportar_csv_sobreaviso(dados, csv_path)
    assert os.path.exists(csv_path)
    with open(csv_path, encoding='utf-8') as f:
        linhas = f.readlines()
    assert 'Dr. A' in ''.join(linhas) and 'Dr. B' in ''.join(linhas)
    # Exporta PDF
    pdf_path = os.path.join(tmp_path, 'relatorio_sobreaviso.pdf')
    exportar_pdf_sobreaviso(dados, pdf_path)
    assert os.path.exists(pdf_path)

def test_relatorio_escalas_por_especializacao(session, setup_db):
    esp, medicos = setup_db
    # Cria plantões e sobreavisos para a especialização
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 6, 15), turno="noturno"))
    session.add(EscalaSobreaviso(medico1_id=medicos[0].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 10)))
    session.commit()
    from app.core.relatorio_escalas_por_especializacao import relatorio_escalas_por_especializacao
    dados = relatorio_escalas_por_especializacao(session, 2024, 6)
    assert len(dados) == 1
    assert dados[0]['especializacao'] == esp.nome
    assert dados[0]['qtd_plantao'] == 2
    assert dados[0]['qtd_sobreaviso'] == 1

def test_relatorio_escalas_por_especializacao_exportacao(tmp_path, session, setup_db):
    esp, medicos = setup_db
    # Cria plantões e sobreavisos para a especialização
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 6, 15), turno="noturno"))
    session.add(EscalaSobreaviso(medico1_id=medicos[0].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 10)))
    session.commit()
    from app.core.relatorio_escalas_por_especializacao import relatorio_escalas_por_especializacao, exportar_csv, exportar_pdf
    dados = relatorio_escalas_por_especializacao(session, 2024, 6)
    # Exporta CSV
    csv_path = tmp_path / 'relatorio_especializacao.csv'
    exportar_csv(dados, str(csv_path))
    assert csv_path.exists()
    with open(csv_path, encoding='utf-8') as f:
        linhas = f.readlines()
    assert esp.nome in ''.join(linhas)
    # Exporta PDF
    pdf_path = tmp_path / 'relatorio_especializacao.pdf'
    exportar_pdf(dados, str(pdf_path))
    assert pdf_path.exists()

def test_relatorio_carga_horaria_medico_csv_pdf(tmp_path, session, setup_db):
    """
    Testa o relatório de carga horária por médico, exportação CSV e PDF.
    """
    esp, medicos = setup_db
    # Cria plantões e sobreavisos para os médicos
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 12), turno="noturno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 6, 15), turno="diurno"))
    session.add(EscalaSobreaviso(medico1_id=medicos[0].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 5), data_final=date(2024, 6, 10)))
    session.add(EscalaSobreaviso(medico1_id=medicos[1].id, especializacao_id=esp.id, data_inicial=date(2024, 6, 15), data_final=date(2024, 6, 20)))
    session.commit()
    from app.core.relatorio_carga_horaria_medico import consulta_carga_horaria_por_medico, exportar_carga_horaria_csv, exportar_carga_horaria_pdf
    dados = consulta_carga_horaria_por_medico(session, 6, 2024)
    # Valida dados
    nomes = [d['nome'] for d in dados]
    assert 'Dr. A' in nomes and 'Dr. B' in nomes
    for d in dados:
        if d['nome'] == 'Dr. A':
            assert d['total_plantoes'] == 2
            assert d['total_sobreavisos'] == 1
        if d['nome'] == 'Dr. B':
            assert d['total_plantoes'] == 1
            assert d['total_sobreavisos'] == 1
    # Exporta CSV
    csv_content = exportar_carga_horaria_csv(dados, 6, 2024)
    csv_path = tmp_path / 'relatorio_carga_horaria.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    assert csv_path.exists()
    with open(csv_path, encoding='utf-8') as f:
        linhas = f.readlines()
    assert 'Dr. A' in ''.join(linhas) and 'Dr. B' in ''.join(linhas)
    # Exporta PDF
    pdf_path = tmp_path / 'relatorio_carga_horaria.pdf'
    exportar_carga_horaria_pdf(dados, 6, 2024, str(pdf_path))
    assert pdf_path.exists()

def test_relatorio_escalas_futuras_csv_pdf(tmp_path, session, setup_db):
    """
    Testa o relatório de escalas futuras (próximos 7 dias), exportação CSV e PDF.
    """
    esp, medicos = setup_db
    hoje = date.today()
    # Cria plantões e sobreavisos futuros
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=hoje + timedelta(days=2), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=hoje + timedelta(days=5), turno="noturno"))
    session.add(EscalaSobreaviso(medico1_id=medicos[2].id, especializacao_id=esp.id, data_inicial=hoje + timedelta(days=3), data_final=hoje + timedelta(days=4)))
    session.commit()
    from app.core.relatorio_escalas_futuras import consultar_escalas_futuras, exportar_escalas_futuras_csv, exportar_escalas_futuras_pdf
    dados = consultar_escalas_futuras(session, dias=7)
    assert any(d['tipo'] == 'plantao' for d in dados)
    assert any(d['tipo'] == 'sobreaviso' for d in dados)
    # Exporta CSV
    csv_content = exportar_escalas_futuras_csv(dados)
    csv_path = tmp_path / 'relatorio_escalas_futuras.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    assert csv_path.exists()
    with open(csv_path, encoding='utf-8') as f:
        linhas = f.readlines()
    assert 'Plantão' in ''.join(linhas) or 'Sobreaviso' in ''.join(linhas)
    # Exporta PDF
    pdf_path = tmp_path / 'relatorio_escalas_futuras.pdf'
    exportar_escalas_futuras_pdf(dados, str(pdf_path))
    assert pdf_path.exists()

def test_relatorio_medicos_por_status_csv_pdf(tmp_path, session, setup_db):
    """
    Testa o relatório de médicos por status (ativos, inativos, afastados), exportação CSV e PDF.
    """
    esp, medicos = setup_db
    # Atualiza status dos médicos
    medicos[0].status = 'ativo'
    medicos[1].status = 'inativo'
    medicos[2].status = 'afastado'
    session.commit()
    from app.core.relatorio_medicos_por_status import consultar_medicos_por_status, exportar_medicos_por_status_csv, exportar_medicos_por_status_pdf
    dados = consultar_medicos_por_status(session)
    nomes = [d['nome'] for d in dados]
    assert 'Dr. A' in nomes and 'Dr. B' in nomes and 'Dr. C' in nomes
    status_set = set([d['status'] for d in dados])
    assert 'ativo' in status_set and 'inativo' in status_set and 'afastado' in status_set
    # Exporta CSV
    csv_content = exportar_medicos_por_status_csv(dados)
    csv_path = tmp_path / 'relatorio_medicos_status.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    assert csv_path.exists()
    with open(csv_path, encoding='utf-8') as f:
        linhas = f.readlines()
    assert 'Dr. A' in ''.join(linhas) and 'Dr. B' in ''.join(linhas) and 'Dr. C' in ''.join(linhas)
    # Exporta PDF
    pdf_path = tmp_path / 'relatorio_medicos_status.pdf'
    exportar_medicos_por_status_pdf(dados, str(pdf_path))
    assert pdf_path.exists()
