"""
Padrão Strategy para múltiplos canais de notificação (e-mail, push, WhatsApp).
Permite trocar ou adicionar canais sem alterar a lógica de envio.
"""
class NotificacaoStrategy:
    def enviar(self, destinatario, mensagem):
        raise NotImplementedError

class EmailStrategy(NotificacaoStrategy):
    def enviar(self, destinatario, mensagem):
        # Implementação real de envio de e-mail
        print(f"E-mail enviado para {destinatario}: {mensagem}")

class PushStrategy(NotificacaoStrategy):
    def enviar(self, destinatario, mensagem):
        # Implementação real de push notification
        print(f"Push enviado para {destinatario}: {mensagem}")

class WhatsAppStrategy(NotificacaoStrategy):
    def enviar(self, destinatario, mensagem):
        # Implementação real de WhatsApp
        print(f"WhatsApp enviado para {destinatario}: {mensagem}")

class Notificador:
    def __init__(self, strategy: NotificacaoStrategy):
        self.strategy = strategy
    def set_strategy(self, strategy: NotificacaoStrategy):
        self.strategy = strategy
    def notificar(self, destinatario, mensagem):
        self.strategy.enviar(destinatario, mensagem)

# Exemplo de uso:
# notificador = Notificador(EmailStrategy())
# notificador.notificar('user@email.com', 'Mensagem de teste')
# notificador.set_strategy(WhatsAppStrategy())
# notificador.notificar('5511999999999', 'Mensagem via WhatsApp')
