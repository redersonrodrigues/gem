# Procedimento para Validação da Estrutura do Banco de Dados (DBeaver/DB Browser SQLite)

## 1. Abrir o DBeaver ou DB Browser SQLite

- Instale o DBeaver (https://dbeaver.io/) ou o DB Browser SQLite (https://sqlitebrowser.org/) caso ainda não tenha.

## 2. Carregar o arquivo `gem.db`

- No DBeaver: clique em “Nova Conexão”, escolha “SQLite”, selecione o arquivo `gem.db` do projeto.
- No DB Browser SQLite: clique em “Abrir Banco de Dados” e selecione o arquivo `gem.db`.

## 3. Visualizar Estrutura das Tabelas

- Navegue até a seção de tabelas e confira se todas as tabelas esperadas (Médicos, Especializações, Escalas, etc.) estão presentes.
- Verifique os campos, tipos de dados, chaves primárias, estrangeiras e constraints de cada tabela.

## 4. Validar Relacionamentos e Integridade

- No visualizador, confira se os relacionamentos (FKs) estão corretos.
- Verifique se triggers e views estão criados conforme o esperado.

## 5. Registrar Evidência

- Tire capturas de tela das estruturas das tabelas, relacionamentos e constraints.
- Salve as imagens na pasta `docs/sql/` ou `docs/validation/` do projeto.

## 6. Documentar a Validação

- Crie um arquivo `docs/sql/validacao_estrutura.md` ou adicione no README da pasta `docs/sql/`:
  - Data da validação
  - Ferramenta utilizada (DBeaver ou DB Browser SQLite)
  - Lista de tabelas e campos validados
  - Observações sobre integridade, constraints, triggers e views
  - Anexe as capturas de tela

## 7. Checklist

- Marque a tarefa como concluída no arquivo `todo.todo` e referencie o local da documentação.
