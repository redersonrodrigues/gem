"""
Padrão Observer para atualização automática de telas ou listeners ao alterar dados relevantes.
Permite que múltiplos observers sejam notificados em tempo real.
"""
class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, data):
        for observer in self._observers:
            observer.update(data)

class EscalaObserver:
    def update(self, data):
        # Aqui pode-se acionar websocket, fila, log ou trigger de atualização de UI
        print(f"Observer notificado: {data}")

# Exemplo de uso:
# observable = Observable()
# observer = EscalaObserver()
# observable.add_observer(observer)
# observable.notify_observers({'escala_id': 1, 'acao': 'criada'})
