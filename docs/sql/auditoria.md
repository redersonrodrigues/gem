# Procedimento de Auditoria do Banco de Dados

## Objetivo

Registrar todas as alterações relevantes (INSERT, UPDATE, DELETE) realizadas nas tabelas principais do banco de dados, garantindo rastreabilidade, segurança e conformidade.

## Estrutura Recomendada

- Criar uma tabela `audit_log` com os campos:
  - id (PK, autoincremento)
  - usuario (texto)
  - data_hora (timestamp)
  - operacao (texto: INSERT, UPDATE, DELETE)
  - tabela (texto)
  - registro_id (inteiro ou texto, conforme PK da tabela auditada)
  - dados_anteriores (JSON ou texto)
  - dados_novos (JSON ou texto)

## Implementação

1. **Triggers SQL**: Criar triggers para cada operação relevante nas tabelas principais (ex: médicos, especializações, escalas), que insiram um registro na `audit_log` a cada alteração.
2. **ORM/SQLAlchemy**: Alternativamente, implementar eventos no SQLAlchemy para registrar alterações via código Python.
3. **Registro de Usuário**: Garantir que o usuário logado seja registrado no campo `usuario`.
4. **Consultas**: Permitir consultas filtrando por data, usuário, operação ou tabela.

## Exemplo de Trigger (SQLite)

```sql
CREATE TRIGGER log_update_medicos
AFTER UPDATE ON medicos
BEGIN
  INSERT INTO audit_log (usuario, data_hora, operacao, tabela, registro_id, dados_anteriores, dados_novos)
  VALUES (CURRENT_USER, datetime('now'), 'UPDATE', 'medicos', OLD.id, json_object('nome', OLD.nome, 'status', OLD.status), json_object('nome', NEW.nome, 'status', NEW.status));
END;
```

## Testes e Evidências

- Realizar operações de inserção, alteração e exclusão nas tabelas auditadas.
- Consultar a tabela `audit_log` e registrar prints dos registros gerados.
- Anexar prints e exemplos de queries nesta documentação.

## Observações

- Adaptar o modelo conforme necessidade de cada tabela.
- Garantir que a auditoria não impacte a performance do banco.
- Manter a documentação atualizada conforme evolução do mecanismo de auditoria.
