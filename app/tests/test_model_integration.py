from Lib.Escala.Database.transaction import Transaction
from app.Model.escala_plantonista import EscalaPlantonista
from app.Model.escala_sobreaviso import EscalaSobreaviso
from app.Model.medico import Medico
from app.Model.especializacao import Especializacao
from app.Model.usuario import Usuario

def test_model_integracao():
    try:
        Transaction.open("escala")

        # Exemplo: buscar um plantonista por id
        escala = EscalaPlantonista.find(1)
        if escala:
            print("Data:", escala.data)
            print("Turno:", escala.turno)
            # Supondo que há relacionamentos ou métodos para buscar médicos
            medico0 = Medico.find(escala.medico_0_id)
            medico1 = Medico.find(escala.medico_1_id)
            print("Médico 0:", medico0.nome if medico0 else "Não encontrado")
            print("Médico 1:", medico1.nome if medico1 else "Não encontrado")
        
        # Exemplo: buscar sobreaviso por id
        sobreaviso = EscalaSobreaviso.find(1)
        if sobreaviso:
            print("Data inicial:", sobreaviso.data_inicial)
            print("Data final:", sobreaviso.data_final)
            # Exemplo de relacionamento com médico e especialização
            medico = Medico.find(sobreaviso.medico_id)
            especializacao = Especializacao.find(sobreaviso.especializacao_id)
            print("Médico:", medico.nome if medico else "Não encontrado")
            print("Especialização:", especializacao.nome if especializacao else "Não encontrada")

        # Exemplo: buscar usuário por id
        usuario = Usuario.find(1)
        if usuario:
            print("Usuário:", usuario.nome)
            print("Login:", usuario.login)
            print("Perfil:", usuario.perfil)

        Transaction.close()
    except Exception as e:
        print("Erro:", str(e))