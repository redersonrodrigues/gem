-- Trigger para atualizar o status do médico para 'inativo' quando não houver escalas futuras
CREATE TRIGGER IF NOT EXISTS atualizar_status_medico_inativo
AFTER UPDATE ON escalas_plantonistas
BEGIN
    UPDATE medicos
    SET status = 'inativo'
    WHERE id = NEW.medico1_id
      AND NOT EXISTS (
        SELECT 1 FROM escalas_plantonistas ep
        WHERE ep.medico1_id = NEW.medico1_id AND ep.data > DATE('now')
      );
END;

-- Trigger para atualizar o status do médico para 'ativo' ao ser incluído em nova escala
CREATE TRIGGER IF NOT EXISTS atualizar_status_medico_ativo
AFTER INSERT ON escalas_plantonistas
BEGIN
    UPDATE medicos
    SET status = 'ativo'
    WHERE id = NEW.medico1_id;
END;

-- Trigger para garantir integridade referencial ao deletar médico (exemplo: impedir exclusão se houver escalas)
CREATE TRIGGER IF NOT EXISTS impedir_delete_medico_com_escalas
BEFORE DELETE ON medicos
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM escalas_plantonistas WHERE medico1_id = OLD.id OR medico2_id = OLD.id) > 0 THEN
            RAISE(ABORT, 'Não é possível excluir médico com escalas associadas')
    END;
END;

-- Trigger para garantir integridade referencial ao deletar especialização
CREATE TRIGGER IF NOT EXISTS impedir_delete_especializacao_com_medicos
BEFORE DELETE ON especializacoes
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM medicos WHERE especializacao_id = OLD.id) > 0 THEN
            RAISE(ABORT, 'Não é possível excluir especialização com médicos associados')
    END;
END;
