# Documentação do Fluxo de Autenticação e Permissões

## Visão Geral

Este documento descreve o fluxo de autenticação, controle de sessão e permissões de acesso na aplicação desktop GEM (Gestão de Escalas Médicas), implementado com PyQt5 e SQLAlchemy, sem dependência de frameworks web.

---

## 1. Estrutura do Modelo de Usuário

- **Arquivo:** `app/models/usuario.py`
- **Campos principais:**

  - `id`: inteiro, chave primária
  - `login`: string, único
  - `senha_hash`: string, hash seguro (bcrypt)
  - `perfil`: string (`admin`, `usuario`, etc)
  - `ativo`: booleano

- **Métodos utilitários:**

  - `verificar_senha(senha)`
  - `is_admin()`
  - `is_active()`

---

## 2. Processo de Login

- Tela de login implementada em `app/views/login.py`.
- Usuário informa login e senha.
- Senha é verificada via método `verificar_senha` (hash seguro).
- Se autenticado, usuário é passado para a sessão principal da aplicação.
- Feedback visual para sucesso/erro.

---

## 3. Controle de Sessão

- Usuário autenticado é mantido em memória enquanto a aplicação está aberta.
- Dados do usuário (nome, perfil) são exibidos na interface principal.
- Sessão pode ser encerrada manualmente (logout) ou por timeout (a implementar).

---

## 4. Permissões e Proteção de Recursos

- Recursos da interface (menus, botões, ações) são exibidos ou habilitados conforme o perfil do usuário.
- Exemplo: menus administrativos visíveis apenas para `admin`.
- Métodos utilitários do modelo `Usuario` facilitam checagem de permissões.

---

## 5. Fluxo de Autenticação e Permissões (Exemplo)

```mermaid
flowchart TD
    Login[Usuário preenche login e senha]
    Verifica[Verifica credenciais no banco (hash)]
    Sucesso{Credenciais válidas?}
    Sessao[Cria sessão do usuário]
    Main[Abre tela principal com permissões]
    Falha[Exibe erro de autenticação]

    Login --> Verifica --> Sucesso
    Sucesso -- Sim --> Sessao --> Main
    Sucesso -- Não --> Falha
```

---

## 6. Recomendações de Segurança

- Senhas nunca são armazenadas em texto plano.
- Usar sempre hash seguro (bcrypt ou argon2).
- Bloquear conta após múltiplas tentativas inválidas (a implementar).
- Expiração de sessão recomendada para ambientes sensíveis.
- Testes automatizados cobrem autenticação e permissões (`tests/integration/test_auth.py`).

---

## 7. Pontos de Extensão

- Adicionar logs de acesso e tentativas de login.
- Implementar gerenciamento de sessões com expiração automática.
- Permissões granulares por recurso/tela.
- Integração futura com autenticação externa (LDAP, OAuth, etc).

---

## 8. Referências

- Código-fonte: `app/models/usuario.py`, `app/views/login.py`, `main.py`
- Testes: `tests/integration/test_auth.py`
- Checklist: `todo.todo`

---

> \*\*Mantenha este documento atualizado conforme novas funcionalidades de autenticação e permissões forem implementadas.
