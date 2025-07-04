# Documentação: Implementação e Testes Automatizados do Modelo Usuario

## 1. Criação da Classe de Modelo

A classe `Usuario` foi criada em `app/Model/usuario.py` para representar os usuários do sistema. Ela implementa métodos para operações CRUD (Create, Read, Update, Delete) e integra-se com a camada de persistência do projeto.

Principais métodos:

- `store()`: Salva ou atualiza o usuário no banco de dados.
- `load(id)`: Carrega um usuário pelo ID.
- `delete()`: Remove o usuário do banco de dados.

## 2. Configuração do Ambiente de Testes

Para garantir que os testes automatizados funcionem corretamente, foram realizados os seguintes ajustes:

- Criação dos arquivos `__init__.py` nas pastas `Lib/`, `Lib/Escala/` e `Lib/Escala/Database/` para que o Python reconheça essas pastas como pacotes.
- Ajuste no início do arquivo de teste (`app/tests/test_usuario.py`) para adicionar o diretório raiz do projeto (`E:\gem`) ao `sys.path`, permitindo que os imports do tipo `from Lib.Escala.Database.transaction import Transaction` funcionem corretamente durante a execução dos testes.

Exemplo do ajuste no início do arquivo de teste:

```python
import sys
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
```

## 3. Implementação do Teste Automatizado

O teste automatizado foi implementado em `app/tests/test_usuario.py` e cobre as seguintes operações:

- **Criação de usuário:** Verifica se um novo usuário pode ser criado e salvo no banco.
- **Busca por ID:** Garante que o usuário criado pode ser recuperado pelo seu ID.
- **Alteração de dados:** Testa a atualização dos dados do usuário.
- **Busca múltipla:** Utiliza `Repository` e `Criteria` para buscar múltiplos usuários com determinado perfil.
- **Contagem:** Verifica se a contagem de usuários com determinado critério está correta.
- **Exclusão:** Testa a remoção do usuário do banco de dados.

Exemplo de função de teste:

```python
def test_criacao_busca_alteracao_delecao_usuario():
    # Criação
    u = Usuario(nome="João Teste", login="joao", senha_hash="1234", perfil="admin", status=1)
    u.store()
    assert u.id is not None

    # Busca por id
    u2 = Usuario().load(u.id)
    assert u2 is not None
    assert u2.nome == "João Teste"

    # Alteração
    u2.nome = "João da Silva"
    u2.store()
    u3 = Usuario().load(u2.id)
    assert u3.nome == "João da Silva"

    # Buscar múltiplos (Repository + Criteria)
    c = Criteria()
    c.add("perfil", "=", "admin")
    repo = Repository(Usuario)
    admins = repo.load(c)
    assert any(a.id == u3.id for a in admins)

    # Contar
    assert repo.count(c) >= 1

    # Deletar
    u3.delete()
    assert Usuario().load(u3.id) is None
```

## 4. Execução dos Testes

Para rodar os testes, utilize o comando:

```
pytest app/tests
```

Certifique-se de estar na raiz do projeto (`E:\gem`) ao executar o comando.

---

Documentação gerada em 03/07/2025.
