# Teste Integrado de Modelos – Explicação

Este documento explica a abordagem utilizada para testes integrados de modelos na aplicação, inspirada na metodologia apresentada por Pablo Dall’Oglio e adaptada para Python.

---

## Objetivo

O teste integrado de modelos serve para verificar:

- O correto funcionamento das operações básicas de entidades (Modelos) do sistema.
- O acesso a atributos simples, derivados e relacionamentos entre entidades (por exemplo, buscar o nome de um médico associado a uma escala).
- A comunicação com o banco de dados através de transações explícitas.
- A robustez do sistema ao lidar com dados reais e possíveis exceções.

---

## Estrutura do Teste

O teste segue os seguintes passos:

1. **Abertura de transação**  
   Antes de qualquer operação sobre o banco de dados, a transação é aberta. Isso garante que as operações sejam atômicas e podem ser revertidas caso ocorra algum erro.

2. **Busca de entidades por ID**  
   Utiliza-se o método `find(id)` das entidades para buscar registros específicos (por exemplo, EscalaPlantonista, EscalaSobreaviso, Medico, Especializacao, Usuario).

3. **Acesso a atributos e relacionamentos**  
   Após obter uma entidade, são acessados tanto os atributos simples quanto os relacionamentos (ex: obter o nome do médico a partir do ID armazenado na escala).

4. **Validação de atributos derivados**  
   Se houver métodos que retornam informações calculadas ou compostas (atributos derivados), estes também são testados.

5. **Tratamento de exceções**  
   Qualquer erro durante o processo é capturado e exibido, facilitando o diagnóstico de problemas.

6. **Fechamento da transação**  
   Ao final do teste, a transação é fechada, garantindo a integridade dos dados.

---

## Exemplo de Código

O teste integrado típico pode ser representado assim:

```python
from Lib.Escala.Database.transaction import Transaction
from app.Model.escala_plantonista import EscalaPlantonista
from app.Model.escala_sobreaviso import EscalaSobreaviso
from app.Model.medico import Medico
from app.Model.especializacao import Especializacao
from app.Model.usuario import Usuario

def test_model_integracao():
    try:
        Transaction.open("escala")

        escala = EscalaPlantonista.find(1)
        if escala:
            print("Data:", escala.data)
            print("Turno:", escala.turno)
            medico0 = Medico.find(escala.medico_0_id)
            medico1 = Medico.find(escala.medico_1_id)
            print("Médico 0:", medico0.nome if medico0 else "Não encontrado")
            print("Médico 1:", medico1.nome if medico1 else "Não encontrado")

        sobreaviso = EscalaSobreaviso.find(1)
        if sobreaviso:
            print("Data inicial:", sobreaviso.data_inicial)
            print("Data final:", sobreaviso.data_final)
            medico = Medico.find(sobreaviso.medico_id)
            especializacao = Especializacao.find(sobreaviso.especializacao_id)
            print("Médico:", medico.nome if medico else "Não encontrado")
            print("Especialização:", especializacao.nome if especializacao else "Não encontrada")

        usuario = Usuario.find(1)
        if usuario:
            print("Usuário:", usuario.nome)
            print("Login:", usuario.login)
            print("Perfil:", usuario.perfil)

        Transaction.close()
    except Exception as e:
        print("Erro:", str(e))
```

---

## Benefícios da abordagem

- **Praticidade:** Permite verificar rapidamente a integração entre as entidades e o banco de dados.
- **Diagnóstico:** Facilita a localização de falhas em relações, dados ou métodos derivados.
- **Base para automação:** Pode ser facilmente adaptado para uso com frameworks de teste automatizado (como pytest) substituindo prints por asserts.

---

## Recomendações

- Garanta que existam registros de teste no banco de dados antes da execução.
- Adapte os IDs utilizados conforme os dados reais para evitar resultados vazios.
- Utilize transações para manter o banco limpo e reverter alterações, se necessário.

---

## Referências

- Pablo Dall’Oglio – Livro: PHP Programando com Orientação a Objetos (Capítulo 8 e exemplos de testes).
- Documentação do projeto GEM – Estrutura de modelos e transações.

---
