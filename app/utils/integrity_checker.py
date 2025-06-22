"""
Módulo utilitário para validação de integridade referencial na interface gráfica.
Verifica se entidades possuem vínculos antes de permitir exclusão/edição.
"""
from app.core.backend_bridge import BackendBridge

class IntegrityChecker:
    def __init__(self, backend: BackendBridge):
        self.backend = backend

    def can_delete_medico(self, medico_id: int) -> bool:
        """Retorna True se o médico pode ser excluído (não possui escalas vinculadas)."""
        escalas = self.backend.get_escalas_by_medico(medico_id)
        return len(escalas) == 0

    def can_delete_especializacao(self, especializacao_id: int) -> bool:
        """Retorna True se a especialização pode ser excluída (não possui médicos vinculados)."""
        medicos = self.backend.get_medicos_by_especializacao(especializacao_id)
        return len(medicos) == 0

    def can_delete_escala(self, escala_id: int) -> bool:
        """Retorna True se a escala pode ser excluída (não possui vínculos impeditivos)."""
        # Exemplo: checar se escala não está em uso em outros módulos
        return True  # Ajustar conforme regras de negócio
