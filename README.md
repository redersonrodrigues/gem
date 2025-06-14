GEM - Gestão de Escalas Médicas
Descrição
O GEM é um sistema para gestão de escalas médicas, cadastro de profissionais, especializações e relatórios, desenvolvido em Python com Flask, SQLite, SQLAlchemy, Bootstrap e PyQt5. O sistema é multiplataforma, responsivo e pode ser executado localmente, sem necessidade de internet.

Funcionalidades
Cadastro, edição e exclusão de médicos, com vínculo a múltiplas especializações
Cadastro, edição e exclusão de especializações médicas
CRUD completo para escalas de Plantonistas (turnos diurno/noturno, dois médicos por turno)
CRUD completo para escalas de Sobreaviso (data, especialidade, médico responsável)
Visualização separada das escalas de plantonistas e sobreavisos
Menu intuitivo com navegação entre tipos de escala
Relacionamento muitos-para-muitos entre médicos e especializações
Popularização em massa de médicos e escalas para testes de performance
Layout responsivo, modo claro/escuro, padronização visual
Testes automatizados com pytest
Documentação técnica com Sphinx
Como usar
Clone o repositório:
Crie e ative o ambiente virtual:
Instale as dependências:
Popule as especializações iniciais:
Execute a aplicação:
Acesse no navegador: http://127.0.0.1:5000
Fluxos principais
Médicos: Menu "Médicos" → cadastrar, editar ou excluir médicos, vinculando especializações.
Especializações: Menu "Especializações" → gerenciar especialidades médicas.
Escalas Plantonistas: Menu "Escala > Plantonista" → visualizar, criar, editar e excluir escalas de plantonistas.
Escalas Sobreaviso: Menu "Escala > Sobreaviso" → visualizar, criar, editar e excluir escalas de sobreaviso.
Estrutura do Projeto
app - Código principal (modelos, controladores, views)
static - Arquivos estáticos (css, js, imagens, bootstrap, fontawesome)
templates - Templates Jinja2
tests - Testes automatizados
docs - Documentação técnica
main.py - Inicialização do Flask
requirements.txt - Dependências
Contribuição
Siga as boas práticas de versionamento (commits claros e frequentes)
Atualize o checklist .todo e este README.md a cada etapa
Documente código e funcionalidades
