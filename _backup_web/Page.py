class Page:
    """
    Superclasse para controles do tipo página; componentes são adicionados via add.
    """

    def __init__(self):
        self.children = []

    def add(self, child):
        self.children.append(child)

    def show(self, param=None):
        content = ''
        for child in self.children:
            # Se o filho for um objeto com __str__, converte para string
            if hasattr(child, '__str__'):
                content += str(child)
            else:
                content += str(child)
        return content
