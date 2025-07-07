# Ajustes e Uso de Componentes PySide6 (Padrão Bootstrap)

## Introdução

Este documento descreve as principais alterações e implementações realizadas para padronizar e facilitar o uso de componentes visuais no projeto desktop PySide6, inspirados no padrão Bootstrap e na lógica de componentes de Pablo Dall'Oglio.

---

## Componentes Implementados

### 1. Button (Lib/Escala/Widgets/Button.py)

- Componente reutilizável para botões estilizados.
- Suporta todos os estilos do Bootstrap 5: `primary`, `secondary`, `success`, `danger`, `warning`, `info`, `light`, `dark`, `link`.
- Possui efeito hover nativo.
- Tamanho se ajusta ao texto, com largura mínima (90px), máxima (300px) e altura padrão (32px).

**Exemplo de uso:**

```python
from Lib.Escala.Widgets.Button import Button

btn1 = Button("Primary", "primary")
btn2 = Button("Success", "success")
btn3 = Button("Danger", "danger")
```

### 2. Panel (Lib/Escala/Widgets/Container/Panel.py)

- Painel visual com header, body e footer.
- Sombra nativa e visual elegante.
- Permite adicionar qualquer widget como conteúdo.

**Exemplo:**

```python
panel = Panel("Título do Painel")
panel.add(widget)
```

### 3. VBox e HBox (Lib/Escala/Widgets/Container/VBox.py, HBox.py)

- Containers verticais e horizontais para organização de layouts.
- Métodos `add(widget)` e `add_stretch()` para flexibilidade.

**Exemplo:**

```python
from Lib.Escala.Widgets.Container import VBox
vbox = VBox()
vbox.add(btn1)
vbox.add(btn2)
vbox.add_stretch()
```

### 4. Message (Lib/Escala/Widgets/Dialog/Message.py)

- Exibe mensagens informativas e de erro ao usuário.
- Inspirado em Pablo Dall'Oglio.

**Exemplo:**

```python
from Lib.Escala.Widgets.Dialog.Message import Message
Message.show('info', 'Mensagem informativa!')
Message.show('error', 'Mensagem de erro!')
```

### 5. Question (Lib/Escala/Widgets/Dialog/Question.py)

- Exibe diálogos de questionamento (Sim/Não) e executa ações conforme resposta.

**Exemplo:**

```python
def on_yes():
    print("Usuário confirmou!")
def on_no():
    print("Usuário negou!")
from Lib.Escala.Widgets.Dialog.Question import Question
Question('Deseja continuar?', on_yes, on_no)
```

---

## Recomendações de Uso

- Sempre utilize os componentes prontos para garantir padronização visual e de comportamento.
- Para botões, prefira o componente `Button` e escolha o estilo desejado.
- Para layouts, utilize `VBox` e `HBox`.
- Para mensagens e perguntas ao usuário, utilize `Message` e `Question`.

## Exemplos de Páginas de Teste

Veja as páginas em `app/Control`:

- `ExemploMessagePage`: Demonstra botões de mensagem.
- `ExemploQuestionPage`: Demonstra diálogo de questionamento.
- `ExemploActionButtonPage`: Demonstra integração de ação com botão.

Essas páginas podem ser acessadas pelo menu lateral em "Testes".

---

## Observações

- Todos os componentes são baseados em widgets nativos PySide6, sem dependência de web ou Bootstrap real.
- O visual e comportamento são inspirados no Bootstrap 5 para facilitar a migração e o uso por desenvolvedores acostumados ao padrão web.
