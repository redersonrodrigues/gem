# Estrutura MVC da aplicação GEM

A aplicação segue o padrão arquitetural MVC (Model-View-Controller), promovendo separação de responsabilidades, escalabilidade e facilidade de manutenção.

## Diretórios e responsabilidades

- **models/**: Modelos de dados, entidades, listeners de auditoria, validações de domínio. Exemplo: `medico.py`, `escala.py`, `audit_log.py`.
- **views/**: Telas, formulários, lógica de interface gráfica (PyQt/PySide), navegação, upload de arquivos, login.
- **core/**: Controladores, regras de negócio, repositórios, consultas, relatórios, serviços, integração backend.
- **components/**: Componentes reutilizáveis de interface (widgets, botões, tabelas customizadas, etc).
- **utils/**: Funções utilitárias, validações, permissões, cache, logger, helpers.
- **templates/**: Templates de interface, relatórios, ou arquivos de layout (pode ser expandido conforme necessidade).
- **config/**: Arquivos de configuração específicos do projeto.

## Boas práticas

- Cada camada deve ser independente e desacoplada.
- Views não devem acessar diretamente Models, sempre via Controllers/Core.
- Components devem ser reutilizáveis e desacoplados da lógica de negócio.
- Utilitários e helpers devem ser genéricos e reaproveitáveis.
- Documentação e comentários explicativos são obrigatórios.

## Observação

Novos arquivos de interface gráfica devem ser criados em `views/` e componentes em `components/`. Siga sempre as convenções PEP8, PEP257 e boas práticas de programação.
