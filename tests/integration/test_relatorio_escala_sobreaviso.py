import os
import tempfile
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.core.relatorio_escala_sobreaviso import consultar_sobreaviso_periodo, exportar_csv, exportar_pdf
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.models.medico import Medico
from app.models.especializacao import Especializacao

def test_consultar_sobreaviso_periodo_limpo(session: Session):
    # Limpa tabelas relevantes
    session.query(EscalaSobreaviso).delete()
    session.query(Medico).delete()
    session.query(Especializacao).delete()
    session.commit()

    # Cria especialização e médico
    esp = Especializacao(nome="Cardiologia")
    session.add(esp)
    session.commit()
    med = Medico(nome="Dr. Sobreaviso", especializacao_id=esp.id, status="ativo")
    session.add(med)
    session.commit()

    # Cria escala de sobreaviso
    data_ini = date.today()
    data_fim = data_ini + timedelta(days=2)
    escala = EscalaSobreaviso(
        data_inicial=data_ini,
        data_final=data_fim,
        medico1_id=med.id,
        especializacao_id=esp.id
    )
    session.add(escala)
    session.commit()

    # Consulta por período abrangendo a escala
    resultado = consultar_sobreaviso_periodo(session, data_ini, data_fim)
    assert len(resultado) == 1
    assert resultado[0]["medico"] == "Dr. Sobreaviso"
    assert resultado[0]["especializacao"] == "Cardiologia"
    assert resultado[0]["data_inicial"] == data_ini
    assert resultado[0]["data_final"] == data_fim

    # Testa exportação CSV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        exportar_csv(resultado, tmp.name)
        tmp.close()
        with open(tmp.name, encoding="utf-8") as f:
            content = f.read()
        assert "Dr. Sobreaviso" in content
        os.unlink(tmp.name)

    # Testa exportação PDF (apenas verifica se arquivo é criado)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        exportar_pdf(resultado, tmp.name)
        tmp.close()
        assert os.path.getsize(tmp.name) > 0
        os.unlink(tmp.name)
