# Documentação: Implementação e Ajustes do Modelo Medico

## 1. Criação da Classe de Modelo

A classe `Medico` foi criada em `app/Model/medico.py` para representar os médicos do sistema. Ela implementa métodos para operações CRUD (Create, Read, Update, Delete) e integra-se com a camada de persistência do projeto.

Principais atributos:

- `id`: Identificador único do médico.
- `nome`: Nome do médico.
- `nome_pj`: Nome da pessoa jurídica associada (opcional).
- `especializacao_id`: Chave estrangeira para a especialização.
- `status`: Situação do médico, podendo ser 'ativo' ou 'inativo'.

## 2. Alinhamento com o Banco de Dados

- O campo correto para status do médico no banco é `status` (tipo TEXT, valores 'ativo' ou 'inativo').
- O modelo e os testes foram ajustados para utilizar o campo `status` (string), removendo o uso de `estatus` (integer), garantindo compatibilidade com a tabela `medico`.

## 3. Ajuste dos Testes Automatizados

O teste automatizado foi implementado em `app/tests/test_medico.py` e cobre as seguintes operações:

- Criação de médicos com diferentes status e especializações.
- Busca de médicos filtrando por especialização e status.
- Busca de médicos pelo nome.
- Contagem de médicos ativos.
- Limpeza dos dados de teste ao final.

Exemplo de uso no teste:

```python
m1 = Medico(nome="Dr. Ana", nome_pj="Ana LTDA", especializacao_id=1, status="ativo")
m1.store()
# ...
c = Criteria()
c.add("especializacao_id", "=", 1)
c.add("status", "=", "ativo")
repo = Repository(Medico)
medicos = repo.load(c)
assert all(m.especializacao_id == 1 and m.status == "ativo" for m in medicos)
```

## 4. Execução dos Testes

Para rodar os testes, utilize o comando:

```
pytest app/tests
```

Certifique-se de estar na raiz do projeto (`E:\gem`) ao executar o comando.

---

Documentação gerada em 03/07/2025.
