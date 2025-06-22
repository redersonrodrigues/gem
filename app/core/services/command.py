"""
Padrão Command para histórico e desfazer/refazer operações críticas.
Permite registrar, executar, desfazer e refazer comandos de alteração de estado.
"""
class Command:
    def execute(self):
        raise NotImplementedError
    def undo(self):
        raise NotImplementedError

class CreateMedicoCommand(Command):
    def __init__(self, repo, medico, user_id):
        self.repo = repo
        self.medico = medico
        self.user_id = user_id
        self._executed = False
    def execute(self):
        self.repo.create(self.medico, self.user_id)
        self._executed = True
    def undo(self):
        if self._executed:
            self.repo.delete(self.medico, self.user_id)
            self._executed = False

class CommandManager:
    def __init__(self):
        self._history = []
        self._redo_stack = []
    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()
    def undo(self):
        if self._history:
            command = self._history.pop()
            command.undo()
            self._redo_stack.append(command)
    def redo(self):
        if self._redo_stack:
            command = self._redo_stack.pop()
            command.execute()
            self._history.append(command)

# Exemplo de uso:
# cmd = CreateMedicoCommand(repo, medico, user_id)
# manager = CommandManager()
# manager.execute(cmd)
# manager.undo()
# manager.redo()
