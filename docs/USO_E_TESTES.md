# GEM - Guia de Uso e Testes

## Como usar o sistema

1. **Login**
   - Acesse `/login`.
   - Usuário admin: `Admin` / `Admin`
   - Usuário comum: `User` / `User`

2. **Cadastro de Médicos**
   - Acesse `/doctors` (apenas admin).
   - Preencha nome, nome fantasia (PJ) e selecione uma ou mais especializações.
   - Todos os campos são obrigatórios e em maiúsculo.

3. **Cadastro de Especializações**
   - Acesse `/specializations` (apenas admin).
   - Informe o nome da especialização (em maiúsculo).

4. **Cadastro de Escalas**
   - Acesse `/schedules`.
   - Para plantonistas: selecione 4 médicos (2 diurno, 2 noturno) para o dia.
   - Para sobreaviso: escolha especialidade, período (quinzenal/semanal), médico e data inicial.
   - O sistema valida duplicidade e regras de negócio.

5. **Relatórios**
   - Acesse `/reports` (em desenvolvimento).

## Testes automatizados

- Execute `pytest` na raiz do projeto para rodar todos os testes.
- Os testes cobrem modelos, CRUD de médicos, especializações, escalas e logs.
- Saída dos testes: consulte `pytest_output.txt`.

## Observações
- Todos os campos de texto são salvos e exibidos em maiúsculo.
- O sistema impede cadastros duplicados e valida regras de escalas.
- Apenas administradores podem cadastrar/editar médicos e especializações.
- O sistema está pronto para validação no ambiente real.

# Uso e Testes da Aplicação com PyQt

## Uso
A aplicação agora utiliza PyQt para a interface gráfica. Para iniciar a aplicação, execute o arquivo `main.py`.

### Funcionalidades principais:
- Cadastro de plantonistas.
- Listagem de plantonistas.
- Edição e exclusão de plantonistas.

## Testes
Os testes existentes continuam válidos para a lógica de backend. Para testar a interface gráfica, utilize ferramentas específicas para testes de GUI, como `pytest-qt` ou `PyQtTest`.

### Executando testes de backend:
```bash
pytest tests/
```
