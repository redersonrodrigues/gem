# Guia de Implementação: AppLoader e ClassLoader no Estilo Pablo Dall'Oglio (Adaptação Python)

Este documento explica detalhadamente como implementar e utilizar um sistema de carregamento dinâmico de classes para aplicações Python, inspirado nos padrões apresentados por Pablo Dall'Oglio em seus livros. O objetivo é garantir que o código da aplicação siga os princípios dos padrões **Front Controller** e **Page Controller**, com separação clara entre classes do framework (biblioteca) e classes da aplicação.

---

## 1. Conceito

### **ClassLoader**  
Responsável por carregar dinamicamente classes do núcleo do framework (pasta `/Lib`).  
- Usa caminhos de módulo e nome da classe.
- Permite centralizar utilitários, helpers e recursos compartilhados.

### **AppLoader**  
Responsável por carregar dinamicamente classes específicas da aplicação (pasta `/app`).  
- Também usa caminhos de módulo e nome da classe.
- Permite o desacoplamento entre o Front Controller e os Page Controllers.

---

## 2. Estrutura Recomendada de Pastas

```
projeto/
  Lib/
    Escala/
      Core/
        class_loader.py
        app_loader.py
      Utils/
        helper.py
  app/
    Control/
      Home.py
      MedicosList.py
    Model/
      Medico.py
    Templates/
      template.html
      assets/
  main.py
```

---

## 3. Implementação

### **3.1. ClassLoader (Lib/Escala/Core/class_loader.py)**

```python
import importlib

class ClassLoader:
    @staticmethod
    def load_class(module_path, class_name):
        """
        Carrega uma classe do framework Lib dado o caminho do módulo e o nome da classe.
        Exemplo: ClassLoader.load_class('Lib.Escala.Utils.helper', 'SomeUtil')
        """
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
```

#### **Exemplo de uso**

```python
from Lib.Escala.Core.class_loader import ClassLoader

SomeUtil = ClassLoader.load_class('Lib.Escala.Utils.helper', 'SomeUtil')
util = SomeUtil()
```

---

### **3.2. AppLoader (Lib/Escala/Core/app_loader.py)**

```python
import importlib

class AppLoader:
    @staticmethod
    def load_app_class(module_path, class_name):
        """
        Carrega uma classe da aplicação app dado o caminho do módulo e o nome da classe.
        Exemplo: AppLoader.load_app_class('app.Control.MedicosList', 'MedicosList')
        """
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
```

#### **Exemplo de uso**

```python
from Lib.Escala.Core.app_loader import AppLoader

ControllerClass = AppLoader.load_app_class('app.Control.MedicosList', 'MedicosList')
controller = ControllerClass()
```

---

## 4. Utilização no Front Controller

No padrão **Front Controller**, a janela principal (ex: `MainWindow`) recebe as ações do usuário e decide qual "Page Controller" deve ser instanciado, usando o AppLoader:

```python
from Lib.Escala.Core.app_loader import AppLoader

class MainWindow(QMainWindow):
    ...
    def show_page(self, class_name):
        try:
            controller_cls = AppLoader.load_app_class(f"app.Control.{class_name}", class_name)
            controller = controller_cls()
            content = controller.show()  # O Page Controller gera o HTML/resultado
        except Exception as e:
            content = f"<h2>Erro ao carregar página '{class_name}'</h2><pre>{e}</pre>"
        html = load_template(context={"content": content, "class": class_name})
        self.browser.setHtml(html, ...)
```

---

## 5. Vantagens

- **Desacoplamento**: O Front Controller não precisa saber onde estão as classes nem fazer imports diretos.
- **Organização**: Framework e aplicação separados, facilitando manutenção e evolução.
- **Escalabilidade**: Adicionar novos controllers ou utilitários é simples, basta criar o arquivo e garantir o nome correto.

---

## 6. Dicas para outros desenvolvedores

- Siga o padrão de nomes de arquivos e classes para facilitar o carregamento dinâmico.
- Use o ClassLoader apenas para classes do framework (`Lib`).
- Use o AppLoader para classes da aplicação (`app`).
- Se precisar criar loaders para outros contextos (ex: plugins), siga o mesmo padrão.
- Em Python, os módulos devem estar no `PYTHONPATH` ou ser localizáveis a partir do diretório do projeto.

---

## 7. Referências

- Pablo Dall'Oglio — "Frameworks para Desenvolvimento em PHP" (cap. 4, 5 e 6)
- [Documentação oficial Python: importlib](https://docs.python.org/3/library/importlib.html)

---

**Resumo**:  
Este padrão permite que sua aplicação Python se beneficie de carregamento dinâmico de classes, separação de responsabilidades e maior organização, seguindo os princípios de arquitetura apresentados por Pablo Dall'Oglio, adaptados do PHP para Python.
