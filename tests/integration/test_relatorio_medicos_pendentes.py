import os
import tempfile
from sqlalchemy.orm import Session
from app.core.relatorio_medicos_pendentes import consultar_medicos_pendentes, exportar_medicos_pendentes_csv, exportar_medicos_pendentes_pdf
from app.models.medico import Medico
from app.models.especializacao import Especializacao

def test_consultar_medicos_pendentes(session: Session):
    # Limpa tabelas
    session.query(Medico).delete()
    session.query(Especializacao).delete()
    session.commit()

    # Cria especialização
    esp = Especializacao(nome="Clínica Geral")
    session.add(esp)
    session.commit()

    # Médico com nome vazio (pendência)
    m1 = Medico(nome="", especializacao_id=esp.id, status="ativo")
    # Médico completo (não deve aparecer)
    m2 = Medico(nome="Dr. Completo", especializacao_id=esp.id, status="ativo")
    session.add_all([m1, m2])
    session.commit()

    resultado = consultar_medicos_pendentes(session)
    nomes = [r["nome"] for r in resultado]
    assert "" in nomes
    assert "Dr. Completo" not in nomes

    # Testa exportação CSV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        exportar_medicos_pendentes_csv(resultado, tmp.name)
        tmp.close()
        with open(tmp.name, encoding="utf-8") as f:
            content = f.read()
        assert content.count(',') > 0  # Deve ter colunas
        os.unlink(tmp.name)

    # Testa exportação PDF (verifica se arquivo é criado)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        exportar_medicos_pendentes_pdf(resultado, tmp.name)
        tmp.close()
        assert os.path.getsize(tmp.name) > 0
        os.unlink(tmp.name)
