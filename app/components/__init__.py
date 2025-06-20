# Componentes reutilizáveis da interface gráfica
# Exemplo: botões customizados, tabelas, widgets, etc.

# Botão customizado
class CustomButton:
    def __init__(self, label, action):
        self.label = label
        self.action = action

    def click(self):
        exec(self.action)

# Tabela simples
class SimpleTable:
    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows

    def display(self):
        # Lógica para exibir a tabela
        pass

# Widget de entrada de texto
class TextInput:
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.value = ""

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value

# Exemplo de uso dos componentes
if __name__ == "__main__":
    # Criando um botão
    button = CustomButton("Clique aqui", "print('Botão clicado!')")
    # Criando uma tabela
    table = SimpleTable(["Coluna 1", "Coluna 2"], [["Linha 1, Col 1", "Linha 1, Col 2"]])
    # Criando um widget de entrada de texto
    text_input = TextInput("Digite algo...")

    # Exibindo os componentes (a lógica de exibição deve ser implementada)
    button.click()
    table.display()
    text_input.set_value("Olá, mundo!")
    print(text_input.get_value())