class Element:
    """
    Classe suporte para tags HTML (p, img, div, etc.), no padrão de Pablo Dall'Oglio.
    Permite adicionar propriedades e filhos, e exibe o HTML correspondente.
    """

    def __init__(self, tagname):
        self.tagname = tagname         # nome da tag
        self._properties = {}          # propriedades do elemento/tag
        self.children = []             # filhos, que podem ser outros elementos ou strings

    def __setattr__(self, name, value):
        # Intercepta atribuições de propriedades dinâmicas (exceto atributos internos)
        if name in ('tagname', '_properties', 'children'):
            super().__setattr__(name, value)
        else:
            self._properties[name] = value

    def __getattr__(self, name):
        # Retorna atributos do dicionário de propriedades, se existirem
        if name in self._properties:
            return self._properties[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def add(self, child):
        """
        Adiciona um elemento filho (objeto ou string)
        """
        self.children.append(child)

    def open(self):
        """
        Exibe a tag de abertura com propriedades
        """
        props = ''
        for name, value in self._properties.items():
            # Converte 'class_' para 'class' no HTML
            html_name = 'class' if name == 'class_' else name
            if isinstance(value, (str, int, float, bool)):
                props += f' {html_name}="{value}"'
        print(f"<{self.tagname}{props}>", end='')

    def close(self):
        """
        Exibe a tag de fechamento
        """
        print(f"</{self.tagname}>")

    def show(self):
        """
        Exibe a tag na tela, junto com seus filhos
        """
        self.open()
        print()  # Nova linha após a abertura da tag

        for child in self.children:
            if hasattr(child, 'show'):
                child.show()
            else:
                print(child, end='')

        self.close()
        print()  # Nova linha após fechamento

    def __str__(self):
        """
        Converte o elemento para string (útil para print(obj))
        """
        from io import StringIO
        import sys

        # Redireciona o print para buffer
        buffer = StringIO()
        stdout = sys.stdout
        sys.stdout = buffer
        self.show()
        sys.stdout = stdout
        return buffer.getvalue()
