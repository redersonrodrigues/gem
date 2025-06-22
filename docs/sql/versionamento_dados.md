# Versionamento de Dados e Histórico de Alterações

## Objetivo

Rastrear todas as alterações relevantes em registros das tabelas principais (médicos, especializações, escalas), permitindo auditoria, rollback e consulta ao histórico de versões.

## Como Funciona

- Cada INSERT, UPDATE ou DELETE em um registro gera uma nova entrada na tabela `historico_versao`.
- O histórico armazena: tabela, id do registro, número da versão, usuário, data/hora e o estado serializado do registro.
- O versionamento é automático via listeners SQLAlchemy, integrado ao mecanismo de auditoria.

## Exemplo de Consulta ao Histórico

```sql
SELECT * FROM historico_versao WHERE tabela = 'medicos' AND registro_id = 1 ORDER BY versao;
```

## Rollback Manual

Para restaurar um registro a uma versão anterior, basta ler o campo `dados` (JSON) e aplicar os valores desejados.

## Integração

- O versionamento está implementado nos modelos: Médico, Especialização, EscalaPlantonista, EscalaSobreaviso.
- O listener está em `app/models/audit_listener.py`.
- Teste automatizado: `tests/unit/test_versionamento.py`.

## Observações

- O versionamento não substitui backup, mas complementa a rastreabilidade.
- O campo `usuario` pode ser integrado ao sistema real de autenticação.
